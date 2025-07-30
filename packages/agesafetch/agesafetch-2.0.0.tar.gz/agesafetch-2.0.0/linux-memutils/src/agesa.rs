// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
/*!
Utilities for finding the [AGESA] version in physical memory (on AMD Zen).

# AGESA

AGESA is a procedure library by AMD embedded into the UEFI firmware of AMD
platforms up to and including Zen 5. It performs _Platform Initialization_,
so it is responsible for CPU startup, memory training, I/O (including PCIe)
configuration, and more.

Because of AGESA's importance for stability _and security_, one may want to
inspect its version, ideally from user space on a running system. Alas, the
Linux kernel does not provide a straightforward interface for this; however,
AGESA's version marker is generally located somewhere in extended memory and
can thus be obtained via a brute-force search as implemented by this module.

<div class="warning">

  [Per coreboot], there are two documented iterations of AGESA:

  * **v5** (or [Arch2008]) for CPU families before Zen (< `17h`)
  * **v9** for Zen and later (≥ `17h`)

  This module supports both, but **v5** was not yet comprehensively tested.

</div>

[AGESA]: https://en.wikipedia.org/wiki/AGESA
[Per coreboot]: https://doc.coreboot.org/soc/amd/family17h.html#introduction
[Arch2008]: https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/specifications/44065_Arch2008.pdf
*/
use std::fs::File;
use std::io::{self, Read, Seek};

use heapless::HistoryBuffer;
use thiserror::Error;

use crate::iomem::{MemoryRegion, MemoryRegionType, parse_proc_iomem};
use crate::reader::SkippingBufReader;

/// An AGESA version found in physical memory.
#[derive(PartialEq)]
pub struct AgesaVersion {
    /// The complete version string (may include trailing whitespace).
    pub version_string: String,
    /// The absolute start address of this version in physical memory.
    pub absolute_address: usize,
    /// The memory region this version is located in.
    pub surrounding_region: MemoryRegion,
}

impl AgesaVersion {
    /// Return this version's offset within its surrounding memory region.
    #[must_use]
    pub fn offset_in_region(&self) -> usize {
        self.absolute_address - self.surrounding_region.start_address
    }
}

#[derive(Error, Debug)]
pub enum SearchError {
    #[error("could not open `/dev/mem`")]
    DevMemUnopenable(#[source] io::Error),

    #[error("could not read memory map from `/proc/iomem`")]
    IomemUnreadable(#[source] io::Error),

    #[error("could not read byte in physical memory from `/dev/mem`")]
    ByteUnreadable(#[source] io::Error),
}

pub type SearchResult = Result<Option<AgesaVersion>, SearchError>;

/// Search for the AGESA version within all `Reserved` memory regions.
///
/// # Errors
///
/// This function will return an error if no memory map could be obtained.
/// It will also return errors for reading from physical memory according
/// to [`find_agesa_version_in_memory_region`].
pub fn find_agesa_version() -> SearchResult {
    let possible_regions =
        get_reserved_regions_in_extended_memory().map_err(SearchError::IomemUnreadable)?;

    for region in possible_regions {
        log::info!("Searching memory region: {region}");
        let maybe_found_version = find_agesa_version_in_memory_region(region)?;
        if maybe_found_version.is_some() {
            return Ok(maybe_found_version);
        }
    }

    Ok(None)
}

/// Search for the AGESA version within the given memory region.
///
/// # Errors
///
/// This function will return an error if `/dev/mem` could not be opened
/// or an unexpected read error occurred during the search.
pub fn find_agesa_version_in_memory_region(region: MemoryRegion) -> SearchResult {
    let file = File::open("/dev/mem").map_err(SearchError::DevMemUnopenable)?;
    let buf_reader = SkippingBufReader::new(file, region.start_address, Some(region.end_address));

    if let Some((version_string, absolute_address)) = find_agesa_version_in_reader(buf_reader)? {
        return Ok(Some(AgesaVersion {
            version_string,
            absolute_address,
            surrounding_region: region,
        }));
    }

    Ok(None)
}

/// The possible states of an ongoing search.
enum SearchState {
    Searching,
    SignatureFound,
    VersionStartFound,
}

/// The signature indicating the start of an AGESA v9 version in memory.
const SIGNATURE_V9: &[u8] = b"AGESA!V";
const SIGNATURE_LENGTH: usize = SIGNATURE_V9.len();

/// The signature indicating the start of an AGESA v5 version in memory.
///
/// Per the Arch2008 spec, this is should be `!!AGESA `; however, on the
/// [Kaveri platform] I tested, it is `!!!AGESA` immediately followed by
/// the version string. The specified prefix should work for both cases.
///
/// [Kaveri platform]: https://github.com/fishbaoz/KaveriPI/blob/master/AGESA/AMD.h#L260
const SIGNATURE_V5: &[u8; SIGNATURE_LENGTH] = b"!!AGESA";

/// Search for the AGESA version within the given buffered reader.
///
/// This returns the found version string and its offset in `buf_reader`.
///
/// # Errors
///
/// This function will return an error if a byte in the reader could not
/// be read (except in case of already-handled permission errors).
pub fn find_agesa_version_in_reader<R: Read + Seek>(
    mut buf_reader: SkippingBufReader<R>,
) -> Result<Option<(String, usize)>, SearchError> {
    let mut version_string = Vec::new();

    let mut search_state = SearchState::Searching;
    let mut search_window: HistoryBuffer<u8, SIGNATURE_LENGTH> = HistoryBuffer::new();

    let mut buffer = [0; 1024];
    loop {
        let bytes_read = buf_reader
            .read(&mut buffer)
            .map_err(SearchError::ByteUnreadable)?;
        if bytes_read == 0 {
            break;
        }

        for (i, &byte) in buffer[..bytes_read].iter().enumerate() {
            match search_state {
                SearchState::Searching => {
                    search_window.write(byte);

                    if search_window.oldest_ordered().eq(SIGNATURE_V9) {
                        // AGESA!V9␀CezannePI-FP6 1.0.1.1␀
                        //       ^
                        search_state = SearchState::SignatureFound;
                    } else if search_window.oldest_ordered().eq(SIGNATURE_V5) {
                        // !!!AGESAKaveriPI        V1.1.0.7    ␀
                        //        ^
                        // For AGESA v5, the version string starts right after
                        // the signature, so there is no null byte to skip to
                        search_state = SearchState::VersionStartFound;
                    }
                }
                SearchState::SignatureFound => {
                    if byte == b'\0' {
                        // AGESA!V9␀CezannePI-FP6 1.0.1.1␀
                        //         ^
                        search_state = SearchState::VersionStartFound;
                    }
                }
                SearchState::VersionStartFound if byte == b'\0' => {
                    // AGESA!V9␀CezannePI-FP6 1.0.1.1␀
                    //                               ^
                    let trimmed_version = version_string.trim_ascii_start();
                    let current_offset = buf_reader.position_in_file() - (bytes_read - i);
                    let version_offset = current_offset - trimmed_version.len();

                    return Ok(Some((
                        String::from_utf8_lossy(trimmed_version).into(),
                        version_offset,
                    )));
                }
                SearchState::VersionStartFound => {
                    version_string.push(byte);
                }
            }
        }
    }

    Ok(None)
}

/// The start address of extended memory.
const EXTENDED_MEM_START: usize = 0x0000_0000_0010_0000;

/// Find and return all `Reserved` regions in [extended memory] (> 1 MiB).
///
/// Testing on a few machines showed that at least one `Reserved` region in
/// extended memory reliably contains the AGESA version – usually the first
/// one at that. Even `Usable` regions may occasionally include it, but the
/// initial (generally small) `Reserved` regions are much faster to search.
///
/// [extended memory]: https://wiki.osdev.org/Memory_Map_(x86)#Extended_Memory_(%3E_1_MiB)
///
/// # Errors
///
/// This function will return an error if `/proc/iomem` could not be read.
pub fn get_reserved_regions_in_extended_memory() -> io::Result<Vec<MemoryRegion>> {
    let all_regions = parse_proc_iomem()?;
    let reserved_high_mem_regions: Vec<MemoryRegion> = all_regions
        .into_iter()
        .filter(|r| r.region_type == MemoryRegionType::Reserved)
        .filter(|r| r.start_address >= EXTENDED_MEM_START)
        .collect();

    Ok(reserved_high_mem_regions)
}

#[cfg(test)]
mod tests {
    use super::*;

    mod found_version {
        use super::*;

        #[test]
        fn offset_in_region_returns_expected_offset() {
            let version = AgesaVersion {
                version_string: "CezannePI-FP6 1.0.1.1".into(),
                absolute_address: 20,
                surrounding_region: MemoryRegion {
                    start_address: 5,
                    end_address: 100,
                    region_type: MemoryRegionType::Reserved,
                },
            };
            assert_eq!(version.offset_in_region(), 15);
        }
    }

    mod find_agesa_version_in_reader {
        use super::*;
        use indoc::formatdoc;
        use rstest::rstest;
        use std::io::Cursor;

        #[rstest]
        #[case::agesa_v9_signature(
            "AGESA!V9\0CezannePI-FP6 1.0.1.1\0",
            "CezannePI-FP6 1.0.1.1",
            37
        )]
        #[case::agesa_v5_signature_arch2008(
            "!!AGESA KaveriPI        V1.1.0.7    \0",
            "KaveriPI        V1.1.0.7    ",
            36
        )]
        #[case::agesa_v5_signature_alternative(
            "!!!AGESAKaveriPI        V1.1.0.7    \0",
            "KaveriPI        V1.1.0.7    ",
            36
        )]
        fn returns_expected_version_string_and_absolute_address(
            #[case] version_in_memory: String,
            #[case] expected_version_string: String,
            #[case] expected_absolute_address: usize,
        ) {
            let file = Cursor::new(formatdoc! {"
                PreceedingUnrelated\0Bytes%p
                {version_in_memory}
                \0SubsequentUnrelatedBytes\0
            "});
            let buf_reader = SkippingBufReader::new(file, 0, None);

            let result = find_agesa_version_in_reader(buf_reader).unwrap();
            assert_eq!(
                result,
                Some((expected_version_string, expected_absolute_address))
            );
        }

        #[test]
        fn returns_none_if_no_agesa_signature_is_present() {
            let file = Cursor::new(b"AESA!V9\0CezannePI-FP6 1.0.1.1\0");
            let buf_reader = SkippingBufReader::new(file, 0, None);

            let result = find_agesa_version_in_reader(buf_reader).unwrap();
            assert_eq!(result, None);
        }

        #[test]
        fn returns_none_if_version_string_does_not_end() {
            let file = Cursor::new(b"AGESA!V9\0CezannePI-FP6 1.0.1.1");
            let buf_reader = SkippingBufReader::new(file, 0, None);

            let result = find_agesa_version_in_reader(buf_reader).unwrap();
            assert_eq!(result, None);
        }
    }
}
