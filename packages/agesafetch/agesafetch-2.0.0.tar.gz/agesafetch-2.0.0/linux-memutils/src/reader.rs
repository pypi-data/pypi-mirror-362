// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
/*!
Semi-efficient reading of physical memory from [`/dev/mem`].

[`/dev/mem`]: https://man7.org/linux/man-pages/man4/mem.4.html
*/
use std::cmp::min;
use std::io::{self, BufRead, ErrorKind, Read, Seek, SeekFrom};

/// The default initial size of the internal buffer in bytes.
const DEFAULT_BUFFER_SIZE: usize = 64 * 1024;

/// A buffering reader that transparently skips inaccessible parts of a file.
///
/// It functions similarly to [`io::BufReader`] in that it fills an internal
/// buffer using larger, infrequent reads but is further capable of handling
/// intermittent permission errors by repeatedly halving the buffer size and
/// attempting another read. Eventually, it will fall back to skipping byte
/// by byte towards the next readable section.
///
/// This will occur for many regions in `/dev/mem` with a brute-force search.
/// Skipping long inaccessible sections is very slow, so that should only be
/// a last resort when no memory map is available.
#[allow(clippy::module_name_repetitions)]
pub struct SkippingBufReader<F: Read + Seek> {
    file: F,

    /// A maximum offset in the `file` to read to; the reader will return 0
    /// bytes (i.e. an EOF) once this is reached.
    max_offset: Option<usize>,

    buffer: Vec<u8>,
    /// The current size of the internal `buffer`.
    buffer_size: usize,
    /// The initial size of the buffer to revert to whenever a read succeeds.
    initial_buffer_size: usize,

    /// The number of bytes at the start of `buffer` set during the last read.
    ///
    /// A read may return fewer bytes than the `buffer_size` (e.g. at the end
    /// of a file) and thus not overwrite the entire buffer. Only those newly
    /// initialized bytes may be used; everything after is stale data.
    valid_bytes_in_buffer: usize,

    /// The position in `buffer` to which bytes have already been "consumed".
    ///
    /// [`SkippingBufReader::read`] may be used with an output buffer smaller
    /// than the number of new bytes available in `buffer`. This keeps track
    /// of such partial reads and determines when new data needs to be read.
    read_position_in_buffer: usize,
}

impl<F: Read + Seek> SkippingBufReader<F> {
    pub fn new(file: F, start_offset: usize, max_offset: Option<usize>) -> Self {
        Self::with_buffer_size(DEFAULT_BUFFER_SIZE, file, start_offset, max_offset)
    }

    /// Create a reader with an internal buffer of the given initial size.
    ///
    /// # Panics
    ///
    /// This function panics if it cannot seek to the given `start_offset`
    /// within `file`.
    pub fn with_buffer_size(
        buffer_size: usize,
        mut file: F,
        start_offset: usize,
        max_offset: Option<usize>,
    ) -> Self {
        file.seek(SeekFrom::Start(start_offset as u64))
            .expect("failed to seek to given start offset");

        Self {
            file,
            max_offset,

            buffer: Vec::with_capacity(buffer_size),
            buffer_size,
            initial_buffer_size: buffer_size,

            valid_bytes_in_buffer: 0,
            read_position_in_buffer: 0,
        }
    }

    fn refill_buffer(&mut self) -> io::Result<usize> {
        loop {
            // If a maximum offset to read to is specified and closer to the
            // current position than the buffer size, reduce the buffer size
            // to only those bytes left to read (down to 0 at the very end)
            if let Some(max_offset) = self.max_offset {
                let seek_position = usize::try_from(self.file.stream_position()?).unwrap();
                let bytes_to_max_offset = max_offset - seek_position;
                self.buffer_size = min(self.buffer_size, bytes_to_max_offset);
            }

            self.buffer.resize(self.buffer_size, 0);

            match self.file.read(&mut self.buffer) {
                Ok(0) => {
                    log::debug!("Reached EOF or maximum offset.");
                    return Ok(0);
                }
                Ok(bytes_read) => {
                    self.buffer_size = self.initial_buffer_size;

                    self.valid_bytes_in_buffer = bytes_read;
                    self.read_position_in_buffer = 0;

                    return Ok(bytes_read);
                }
                Err(e) if e.kind() == ErrorKind::PermissionDenied => {
                    if self.buffer_size > 1 {
                        self.buffer_size /= 2;
                    } else {
                        // Down to a 1-byte buffer; give up on this byte
                        self.file.seek_relative(1)?;
                    }
                }
                Err(e) => return Err(e),
            }
        }
    }

    /// Return the current read position in the file.
    ///
    /// # Note
    ///
    /// This is the position a subsequent call to `read()` will return bytes
    /// from (or refill the buffer if empty). It is distinct from the actual
    /// seek position in the file, which reflects the end of the latest read
    /// performed to fill the buffer.
    ///
    /// # Panics
    ///
    /// This function panics if the current seek position in the underlying
    /// reader cannot be obtained.
    #[must_use]
    pub fn position_in_file(&mut self) -> usize {
        let seek_position = self
            .file
            .stream_position()
            .expect("obtaining the current seek position should always succeed");
        let unread_bytes_in_buffer = self.valid_bytes_in_buffer - self.read_position_in_buffer;

        usize::try_from(seek_position).unwrap() - unread_bytes_in_buffer
    }
}

impl<F: Read + Seek> BufRead for SkippingBufReader<F> {
    fn fill_buf(&mut self) -> io::Result<&[u8]> {
        if self.read_position_in_buffer >= self.valid_bytes_in_buffer {
            log::trace!("No unread bytes in buffer; refilling it...");
            let bytes_read = self.refill_buffer()?;
            log::trace!("Refilled buffer with {bytes_read} bytes.");

            if bytes_read == 0 {
                return Ok(&[]);
            }
        }

        let unread_bytes = &self.buffer[self.read_position_in_buffer..self.valid_bytes_in_buffer];
        Ok(unread_bytes)
    }

    fn consume(&mut self, amt: usize) {
        self.read_position_in_buffer += amt;
    }
}

impl<F: Read + Seek> Read for SkippingBufReader<F> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        // Fetch all unread bytes from the internal buffer, refilling
        // it if needed
        let mut available_bytes = self.fill_buf()?;
        // Pull as many available bytes as fit into the output buffer
        let no_of_bytes_read = available_bytes.read(buf)?;
        // Advance the cursor in the internal buffer by the number of
        // bytes that were used
        self.consume(no_of_bytes_read);

        Ok(no_of_bytes_read)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn position_in_file_returns_expected_position() {
        let file = Cursor::new("abcdefghijklmnopqrst");
        let mut reader = SkippingBufReader::with_buffer_size(8, file, 0, None);

        // This number of bytes to read falls into the last (partial) buffer
        // fill, making it suitable for testing that the result is not based
        // on the buffer's size but the actual number of _valid_ bytes in it
        let mut data = [0; 18];
        reader.read_exact(&mut data).unwrap();
        assert_eq!(reader.position_in_file(), 18);
    }

    #[test]
    fn stops_reading_at_max_offset_if_specified() {
        let file = Cursor::new("abcdefghijklmnopqrst");
        let mut reader = SkippingBufReader::new(file, 0, Some(10));

        let mut data = Vec::new();
        reader.read_to_end(&mut data).unwrap();
        assert_eq!(data, b"abcdefghij");
    }

    struct CursorWithError {
        inner: Cursor<Vec<u8>>,
        bad_byte_position: usize,
        error_kind: ErrorKind,
    }

    impl Read for CursorWithError {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            let current_position = usize::try_from(self.inner.position()).unwrap();
            let read_end_position = current_position + buf.len();

            if (current_position..read_end_position).contains(&self.bad_byte_position) {
                return Err(io::Error::from(self.error_kind));
            }

            self.inner.read(buf)
        }
    }

    impl Seek for CursorWithError {
        fn seek(&mut self, pos: SeekFrom) -> io::Result<u64> {
            self.inner.seek(pos)
        }
    }

    #[test]
    fn skips_byte_for_which_read_returns_a_permission_error() {
        let file = CursorWithError {
            inner: Cursor::new("abcdefghijklmnopqrst".as_bytes().to_vec()),
            bad_byte_position: 4,
            error_kind: ErrorKind::PermissionDenied,
        };
        let mut reader = SkippingBufReader::new(file, 0, None);

        let mut data = Vec::new();
        reader.read_to_end(&mut data).unwrap();
        assert_eq!(data, b"abcdfghijklmnopqrst");
    }

    #[test]
    fn does_not_ignore_error_kinds_other_than_permission_denied() {
        let file = CursorWithError {
            inner: Cursor::new("abcdefghijklmnopqrst".as_bytes().to_vec()),
            bad_byte_position: 4,
            error_kind: ErrorKind::ResourceBusy,
        };
        let mut reader = SkippingBufReader::new(file, 0, None);

        let mut data = Vec::new();
        let result = reader.read_to_end(&mut data);
        assert_eq!(result.map_err(|e| e.kind()), Err(ErrorKind::ResourceBusy));
    }
}
