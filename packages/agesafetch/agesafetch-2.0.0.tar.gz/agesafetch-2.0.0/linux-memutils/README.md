# linux-memutils

[![crates.io Version][Version Badge]][crates.io]
[![MSRV: 1.85.0][MSRV Badge]][Rust 1.85.0]
[![docs.rs Status][docs.rs Badge]][docs.rs]
[![License: MIT][License Badge]][LICENSE]
[![REUSE Status][REUSE Badge]][REUSE Status]

[crates.io]: https://crates.io/crates/linux-memutils
[Version Badge]: https://img.shields.io/crates/v/linux-memutils
[Rust 1.85.0]: https://releases.rs/docs/1.85.0/
[MSRV Badge]: https://img.shields.io/crates/msrv/linux-memutils
[docs.rs Badge]: https://img.shields.io/docsrs/linux-memutils
[License Badge]: https://img.shields.io/gitlab/license/BVollmerhaus%2Fagesafetch
[REUSE Status]: https://api.reuse.software/info/gitlab.com/BVollmerhaus/agesafetch
[REUSE Badge]: https://api.reuse.software/badge/gitlab.com/BVollmerhaus/agesafetch

Basic utilities for reading from physical memory on Linux.

## Features

This crate provides modules for:

* Parsing the physical memory map provided by Linux's `/proc/iomem` file.
* Tolerantly reading data from the `/dev/mem` character device file without
  erroring out on inaccessible bytes.
* Searching for the system firmware's [AGESA] version in physical memory.

[AGESA]: https://en.wikipedia.org/wiki/AGESA

## Usage

Add the dependency to your `Cargo.toml`:

```toml
[dependencies]
linux-memutils = "2.0.0"
```

### Examples

#### Obtaining memory regions in `/proc/iomem`

```rust
use linux_memutils::iomem;

fn main() {
    let memory_map = iomem::parse_proc_iomem().unwrap();

    let third_memory_region = &memory_map[2];
    println!("{third_memory_region}");
    // => [0x000000000009f000-0x000000000009ffff] (Reserved)
}
```

#### Reading bytes from a region in physical memory

```rust
use linux_memutils::reader;
use std::fs::File;

fn main() {
    // [...]

    let file = File::open("/dev/mem").unwrap();
    let reader = reader::SkippingBufReader::new(
        file,
        third_memory_region.start_address,
        Some(third_memory_region.end_address),
    );

    // Our `reader` can now be used similarly to an io:BufReader,
    // the key difference being that it skips inaccessible bytes
}
```

#### Finding the system firmware's embedded AGESA version

```rust
use linux_memutils::agesa;

fn main() {
    match agesa::find_agesa_version().unwrap() {
        Some(found_version) => {
            println!("{}", found_version.version_string)
        }
        None => eprintln!("Did not find AGESA version.")
    }
}
```

⚠️ _Note that these examples need to be run with elevated privileges._

## Documentation

As usual, the documentation for this library can be found on [docs.rs].

## Author

* [Benedikt Vollmerhaus](https://gitlab.com/BVollmerhaus)

## License

This project is licensed under the MIT license. See the [LICENSE] file
for more information.

[docs.rs]: https://docs.rs/linux-memutils
[LICENSE]: https://gitlab.com/BVollmerhaus/agesafetch/blob/master/LICENSE
