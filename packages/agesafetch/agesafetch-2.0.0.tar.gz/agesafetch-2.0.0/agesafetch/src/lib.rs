// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
#[cfg(feature = "python-bindings")]
mod python;

use std::error::Error;
use std::ffi::OsString;
use std::io::{self, IsTerminal};
use std::sync::LazyLock;
use std::time::{Duration, Instant};

use caps::{CapSet, Capability};
use clap::Parser;
use colored::{ColoredString, Colorize};
use indoc::{eprintdoc, indoc, printdoc};
use linux_memutils::agesa::{
    AgesaVersion, SearchError, SearchResult, find_agesa_version,
    find_agesa_version_in_memory_region, get_reserved_regions_in_extended_memory,
};
use linux_memutils::iomem::MemoryRegion;

#[derive(Parser, Debug)]
#[command(version, about, after_help = indoc! {"
    Exit Codes:
      0: An AGESA version was found
      1: No version was found in any searched memory region
      2: /proc/iomem could not be read, e.g. due to insufficient permissions
      3: /dev/mem could not be opened, e.g. due to insufficient permissions
      4: An unhandled error occurred while reading a byte in /dev/mem
"})]
struct Cli {
    /// Print only the found version (default if not in a TTY)
    #[arg(short, long, conflicts_with = "verbose")]
    quiet: bool,
    /// Print further information and a closing search summary
    #[arg(short, long)]
    verbose: bool,
}

#[repr(u8)]
pub enum CliExitCode {
    VersionFound = 0,
    NoVersionFound = 1,
    ProcIomemReadFailure = 2,
    DevMemOpenFailure = 3,
    DevMemReadFailure = 4,
}

static STATUS_PREFIX: LazyLock<ColoredString> = LazyLock::new(|| "::".blue().bold());
static RESULT_PREFIX: LazyLock<ColoredString> = LazyLock::new(|| "->".yellow().bold());
static ERROR_PREFIX: LazyLock<ColoredString> = LazyLock::new(|| "ERR".red().bold());

#[must_use]
#[allow(clippy::missing_panics_doc)]
pub fn run_cli(args_os: Vec<OsString>) -> CliExitCode {
    let cli = Cli::parse_from(args_os);

    if !caps::has_cap(None, CapSet::Effective, Capability::CAP_SYS_ADMIN).unwrap() {
        eprintdoc! {"
            {} Missing privileges for reading a memory map from /proc/iomem.
                Please run agesafetch as root or add the SYS_ADMIN capability.
            ",
            *ERROR_PREFIX,
        }
        return CliExitCode::ProcIomemReadFailure;
    }

    match find_and_print_agesa_version(&cli) {
        Ok(Some(_)) => CliExitCode::VersionFound,
        Ok(None) => CliExitCode::NoVersionFound,
        Err(SearchError::IomemUnreadable(_)) => {
            eprintln!(
                "{} Could not read /proc/iomem. Are its permissions correct?",
                *ERROR_PREFIX,
            );
            CliExitCode::ProcIomemReadFailure
        }
        Err(SearchError::DevMemUnopenable(_)) => {
            eprintdoc! {"
                {} Could not open /dev/mem.
                    Please run agesafetch as root or add suitable capabilities.
                ",
                *ERROR_PREFIX,
            }
            CliExitCode::DevMemOpenFailure
        }
        Err(err @ SearchError::ByteUnreadable(_)) => {
            eprintln!(
                "{} Unhandled error while reading byte in physical memory: {}",
                *ERROR_PREFIX,
                err.source().expect("search error should have a source"),
            );
            CliExitCode::DevMemReadFailure
        }
    }
}

fn find_and_print_agesa_version(cli: &Cli) -> SearchResult {
    if !io::stdout().is_terminal() || cli.quiet {
        let maybe_found_version = find_agesa_version()?;
        match maybe_found_version {
            Some(ref found_version) => println!("{}", found_version.version_string.trim_end()),
            None => eprintln!("Did not find AGESA version."),
        }
        return Ok(maybe_found_version);
    }

    let reserved_regions =
        get_reserved_regions_in_extended_memory().map_err(SearchError::IomemUnreadable)?;

    if cli.verbose {
        println!(
            "{} Memory map lists {} regions of type {} in extended memory.",
            *STATUS_PREFIX,
            reserved_regions.len().to_string().blue(),
            "Reserved".italic(),
        );
    }

    let search_start_time = Instant::now();
    let maybe_found_version = search_regions_and_print_statuses(reserved_regions)?;
    let search_duration = search_start_time.elapsed();

    match maybe_found_version {
        Some(ref found_version) => {
            println!(
                "{} Found AGESA version: {}",
                *RESULT_PREFIX,
                found_version.version_string.trim_end().green().bold(),
            );

            if cli.verbose {
                print_search_summary(found_version, &search_duration);
            }
        }
        None => eprintln!("{} Did not find AGESA version.", *RESULT_PREFIX),
    }

    Ok(maybe_found_version)
}

/// Sequentially search each of the given regions for an AGESA version.
///
/// This returns as soon as a version is found or an error has occurred.
fn search_regions_and_print_statuses(regions: Vec<MemoryRegion>) -> SearchResult {
    for (i, region) in regions.into_iter().enumerate() {
        println!(
            "{} Searching {} region {} ({} KiB)...",
            *STATUS_PREFIX,
            region.region_type.to_string().italic(),
            format!("#{}", i + 1).blue(),
            region.size() / 1024,
        );

        match find_agesa_version_in_memory_region(region) {
            Ok(None) => (),
            result => return result,
        }
    }

    Ok(None)
}

/// Print a concise summary with information about the completed search.
#[allow(clippy::cast_precision_loss)]
fn print_search_summary(found_version: &AgesaVersion, search_duration: &Duration) {
    printdoc! {"
        {} Search Summary:
           * Found at Physical Address: {:#x} (in {dev_mem})
           * Surrounding Memory Region: {}
           * Region Size:               {} KiB
           * Bytes Processed in Region: {} KiB
           * Search Time:               {:.1} ms
        ",
        *STATUS_PREFIX,
        found_version.absolute_address,
        found_version.surrounding_region,
        found_version.surrounding_region.size() / 1024,
        found_version.offset_in_region() / 1024,
        search_duration.as_micros() as f64 / 1000.0,
        dev_mem = "/dev/mem".dimmed(),
    }
}
