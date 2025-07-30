// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
/*!
Parsing of the physical memory map provided by `/proc/iomem`.

The `/proc/iomem` file exposes the kernel's resource tree and thus a map of
physical memory to user space, making it very useful for gracefully reading
specific regions of memory from [`/dev/mem`].

# Background

The Linux kernel maintains a _resource tree_ with the memory address ranges
allocated to every resource (RAM, devices, and so on).

The first additions to this tree are made during early boot when the system
firmware supplies its initial memory map to the kernel via [E820] (BIOS) or
[GetMemoryMap()] (UEFI). The kernel will practically always modify this map
further (based on known quirks or custom `memmap` overrides, for instance)
before registering its specified memory regions in the tree.

Additional address ranges are allocated for device [MMIO], so the tree will
contain not just entries for the above memory map (with [ACPI Address Range
Types] such as `Reserved`) but also more arbitrarily named devices (such as
`IOAPIC 0` or `PCI Bus <ID>`).

## Excerpt of `/proc/iomem`

> Notice how the address range names include both human-readable ACPI types
> and MMIO devices.

```text
00000000-00000fff : Reserved            // Real-Mode Address Space (< 1 MiB)
00001000-0009efff : System RAM
0009f000-0009ffff : Reserved
000e0000-000fffff : Reserved
  000a0000-000effff : PCI Bus 0000:00
  000f0000-000fffff : System ROM
00100000-09bfffff : System RAM          // Extended Memory (> 1 MiB)
[~]
cad7e000-cbd7dfff : ACPI Non-volatile Storage
  cbc37000-cbc37fff : USBC000:00
cbd7e000-cbdfdfff : ACPI Tables
[~]
fc000000-fdffffff : PCI Bus 0000:00
  [~ Other devices on the PCIe bus ~]
  fd900000-fd9fffff : PCI Bus 0000:01
    fd900000-fd903fff : 0000:01:00.0
      fd900000-fd903fff : nvme
  fdf00000-fdf7ffff : amd_iommu
feb00000-feb00007 : SB800 TCO
fec00000-fec003ff : IOAPIC 0
[~]
100000000-72e2fffff : System RAM
  38a400000-38b7fffff : Kernel code
  38b800000-38c532fff : Kernel rodata
  38c600000-38c88cf7f : Kernel data
  38d20e000-38d5fffff : Kernel bss
```

[`/dev/mem`]: https://man7.org/linux/man-pages/man4/mem.4.html
[E820]: https://uefi.org/specs/ACPI/6.5/15_System_Address_Map_Interfaces.html#int-15h-e820h-query-system-address-map
[GetMemoryMap()]: https://uefi.org/specs/ACPI/6.5/15_System_Address_Map_Interfaces.html#uefi-getmemorymap-boot-services-function
[MMIO]: https://docs.kernel.org/driver-api/device-io.html#memory-mapped-io
[ACPI Address Range Types]: https://uefi.org/specs/ACPI/6.5/15_System_Address_Map_Interfaces.html#address-range-types
*/
use std::fmt::{self, Debug, Display, Formatter};
use std::sync::LazyLock;
use std::{fs, io};

use regex_lite::Regex;
use thiserror::Error;

/// A region in physical memory as indicated in the memory map.
#[derive(Debug, PartialEq)]
pub struct MemoryRegion {
    pub start_address: usize,
    pub end_address: usize,
    pub region_type: MemoryRegionType,
}

impl MemoryRegion {
    /// Return the length of this memory region in bytes.
    #[must_use]
    pub fn size(&self) -> usize {
        self.end_address - self.start_address
    }
}

impl Display for MemoryRegion {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "[{:#018x}-{:#018x}] ({:?})",
            self.start_address, self.end_address, self.region_type
        )
    }
}

/// The types of memory address ranges distinguished by the kernel.
///
/// These largely correspond to the _ACPI Address Range Types_ as defined in
/// the kernel's [`e820_type`] enum (with some minor changes).
///
/// UEFI provides even more fine-grained _Memory Types_, but the kernel maps
/// those to the basic ACPI types in [`do_add_efi_memmap`] (according to the
/// specified [UEFI–ACPI Mapping]).
///
/// [`e820_type`]: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/arch/x86/include/asm/e820/types.h?h=v6.12#n10
/// [`do_add_efi_memmap`]: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/arch/x86/platform/efi/efi.c?h=v6.12#n121
/// [UEFI–ACPI Mapping]: https://uefi.org/specs/ACPI/6.5/15_System_Address_Map_Interfaces.html#uefi-memory-types-and-mapping-to-acpi-address-range-types
#[derive(Debug, PartialEq)]
pub enum MemoryRegionType {
    Usable,
    Reserved,
    SoftReserved,
    AcpiData,
    AcpiNvs,
    Unusable,
    Persistent,
    /// An E820 type not known to the kernel.
    Unknown,

    /// Any type not part of the ACPI specification, such as an MMIO range.
    NonAcpi(String),
}

impl From<&str> for MemoryRegionType {
    /// Return the enum variant for a given address range type as printed
    /// by the kernel.
    ///
    /// This mapping is derived from the [`e820_type_to_string`] function.
    ///
    /// [`e820_type_to_string`]: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/arch/x86/kernel/e820.c?h=v6.12#n1063
    fn from(s: &str) -> Self {
        match s {
            "System RAM" => Self::Usable,
            "Reserved" => Self::Reserved,
            "Soft Reserved" => Self::SoftReserved,
            "ACPI Tables" => Self::AcpiData,
            "ACPI Non-volatile Storage" => Self::AcpiNvs,
            "Unusable memory" => Self::Unusable,
            "Persistent Memory" | "Persistent Memory (legacy)" => Self::Persistent,
            "Unknown E820 type" => Self::Unknown,

            _ => Self::NonAcpi(s.into()),
        }
    }
}

impl Display for MemoryRegionType {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

#[derive(Error, Debug, PartialEq)]
pub enum ParseError {
    #[error("line of memory map is not in iomem format: '{0}'")]
    InvalidFormat(String),
    #[error("line of memory map has invalid start address: {0}")]
    InvalidStartAddress(String),
    #[error("line of memory map has invalid end address: {0}")]
    InvalidEndAddress(String),
}

/// Directly read and parse `/proc/iomem` to a vector of [`MemoryRegion`]s.
///
/// # Errors
///
/// This function will return an error if `/proc/iomem` could not be read.
///
/// # Panics
///
/// This function panics if the file contains unexpected lines or ones with
/// invalid memory addresses. As this should **never** happen on a standard
/// Linux kernel, it may indicate a somewhat corrupt system state.
#[allow(clippy::module_name_repetitions)]
pub fn parse_proc_iomem() -> io::Result<Vec<MemoryRegion>> {
    let contents = fs::read_to_string("/proc/iomem")?;
    let memory_regions =
        parse_iomem_map(&contents).expect("/proc/iomem should contain only valid lines");
    Ok(memory_regions)
}

/// Parse the given `iomem`-style memory map to a vector of [`MemoryRegion`]s.
///
/// # Errors
///
/// This function will return an error if the memory map could not be parsed.
pub fn parse_iomem_map(content: &str) -> Result<Vec<MemoryRegion>, ParseError> {
    let mut memory_regions = Vec::new();

    for line in content.lines().filter(|l| !l.is_empty()) {
        // This parsing cannot yet represent the resource hierarchy, so
        // ignore sub-resources rather than potentially misrepresenting
        // the memory map (e.g. for a "Reserved" within an MMIO region)
        if line.starts_with(' ') {
            continue;
        }

        let region = parse_iomem_map_line(line)?;
        memory_regions.push(region);
    }

    Ok(memory_regions)
}

/// A regex for lines of an `iomem`-style memory map.
static IOMEM_MAP_LINE_REGEX: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"(\w+)-(\w+) : (.+)").unwrap());

/// Parse the given line of an `iomem`-style memory map to a [`MemoryRegion`].
fn parse_iomem_map_line(line: &str) -> Result<MemoryRegion, ParseError> {
    let Some((_full, [start_address, end_address, region_type])) = IOMEM_MAP_LINE_REGEX
        .captures(line)
        .map(|caps| caps.extract())
    else {
        return Err(ParseError::InvalidFormat(line.into()));
    };

    let Ok(start_address) = usize::from_str_radix(start_address, 16) else {
        return Err(ParseError::InvalidStartAddress(start_address.into()));
    };
    let Ok(end_address) = usize::from_str_radix(end_address, 16) else {
        return Err(ParseError::InvalidEndAddress(end_address.into()));
    };

    let memory_region = MemoryRegion {
        start_address,
        end_address,
        region_type: MemoryRegionType::from(region_type),
    };

    Ok(memory_region)
}

#[cfg(test)]
#[allow(clippy::unreadable_literal)]
mod tests {
    use super::*;
    use indoc::indoc;

    mod memory_region {
        use super::*;

        #[test]
        fn size_returns_correct_size_of_region_in_bytes() {
            let region = MemoryRegion {
                start_address: 0x00100000,
                end_address: 0x09bfffff,
                region_type: MemoryRegionType::Usable,
            };
            assert_eq!(region.size(), 162_529_279);
        }

        #[test]
        fn is_formatted_as_expected_human_readable_string() {
            let region = MemoryRegion {
                start_address: 0x00100000,
                end_address: 0x09bfffff,
                region_type: MemoryRegionType::Usable,
            };
            assert_eq!(
                region.to_string(),
                "[0x0000000000100000-0x0000000009bfffff] (Usable)"
            );
        }
    }

    mod parse_iomem_map {
        use super::*;

        /// A dummy `iomem`-style memory map comprising all ACPI types.
        const PROC_IOMEM_MAP: &str = indoc! {"
            00000080-000000ff : System RAM
            00000100-000001ff : Reserved
              00000180-000001bf : PCI Bus 0000:00
              000001c0-000001ff : System ROM
            00000200-000003ff : Soft Reserved
            00000400-000007ff : ACPI Tables
            00000800-00000fff : ACPI Non-volatile Storage
            00001000-00001fff : Unusable memory
            00002000-00003fff : Persistent Memory
            00004000-00007fff : Persistent Memory (legacy)
            00008000-0000ffff : Unknown E820 type
            00010000-0001ffff : PCI ECAM 0000
              00010000-0001ffff : Reserved
                00010000-0001ffff : pnp 00:00
        "};

        #[test]
        fn returns_vector_of_expected_memory_regions() {
            let regions = parse_iomem_map(PROC_IOMEM_MAP);
            let expected_regions = vec![
                (0x000080, MemoryRegionType::Usable),
                (0x000100, MemoryRegionType::Reserved),
                (0x000200, MemoryRegionType::SoftReserved),
                (0x000400, MemoryRegionType::AcpiData),
                (0x000800, MemoryRegionType::AcpiNvs),
                (0x001000, MemoryRegionType::Unusable),
                (0x002000, MemoryRegionType::Persistent),
                (0x004000, MemoryRegionType::Persistent),
                (0x008000, MemoryRegionType::Unknown),
                (0x010000, MemoryRegionType::NonAcpi("PCI ECAM 0000".into())),
            ]
            .into_iter()
            .map(|(start_address, region_type)| MemoryRegion {
                start_address,
                end_address: start_address * 2 - 1,
                region_type,
            })
            .collect();

            assert_eq!(regions, Ok(expected_regions));
        }
    }

    mod parse_iomem_map_line {
        use super::*;

        #[test]
        fn returns_expected_memory_region_for_line_with_acpi_type() {
            let result = parse_iomem_map_line("00100000-09bfffff : System RAM");
            assert_eq!(
                result,
                Ok(MemoryRegion {
                    start_address: 0x00100000,
                    end_address: 0x09bfffff,
                    region_type: MemoryRegionType::Usable,
                })
            );
        }

        #[test]
        fn returns_expected_memory_region_for_line_with_non_acpi_type() {
            let result = parse_iomem_map_line("d0000000-f7ffffff : PCI Bus 0000:00");
            assert_eq!(
                result,
                Ok(MemoryRegion {
                    start_address: 0xd0000000,
                    end_address: 0xf7ffffff,
                    region_type: MemoryRegionType::NonAcpi("PCI Bus 0000:00".into()),
                })
            );
        }

        #[test]
        fn returns_invalid_format_error_if_line_is_not_in_iomem_format() {
            let invalid_line = "This is not an iomem memory map line.";
            assert_eq!(
                parse_iomem_map_line(invalid_line),
                Err(ParseError::InvalidFormat(invalid_line.into()))
            );
        }

        #[test]
        fn returns_invalid_start_address_error_if_start_address_is_not_hex() {
            assert_eq!(
                parse_iomem_map_line("0000yyyy-00000fff : Reserved"),
                Err(ParseError::InvalidStartAddress("0000yyyy".into()))
            );
        }

        #[test]
        fn returns_invalid_end_address_error_if_end_address_is_not_hex() {
            assert_eq!(
                parse_iomem_map_line("00000000-0000zzzz : Reserved"),
                Err(ParseError::InvalidEndAddress("0000zzzz".into()))
            );
        }
    }
}
