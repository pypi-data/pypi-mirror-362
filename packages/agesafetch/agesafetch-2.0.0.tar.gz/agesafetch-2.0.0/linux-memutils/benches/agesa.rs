// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
use std::io::Cursor;

use divan::counter::BytesCount;

use linux_memutils::agesa;
use linux_memutils::reader::SkippingBufReader;

fn main() {
    divan::main();
}

#[divan::bench]
fn find_agesa_version_in_reader(bencher: divan::Bencher) {
    let total_bytes: usize = 4 * 1024 * 1024;
    let version_in_mem = b"AGESA!V9\0CezannePI-FP6 1.0.1.1\0";
    let bytes_before = total_bytes - version_in_mem.len();

    bencher
        .counter(BytesCount::new(total_bytes))
        .with_inputs(|| {
            let mut data = Vec::with_capacity(total_bytes);
            data.extend(vec![b'\0'; bytes_before]);
            data.extend(version_in_mem);

            let file = Cursor::new(data);
            SkippingBufReader::new(file, 0, None)
        })
        .bench_values(|buf_reader| {
            agesa::find_agesa_version_in_reader(buf_reader).unwrap();
        });
}
