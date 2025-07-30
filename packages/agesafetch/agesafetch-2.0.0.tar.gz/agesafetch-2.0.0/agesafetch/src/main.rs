// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
use std::env;
use std::process::ExitCode;

use agesafetch::run_cli;

fn main() -> ExitCode {
    let exit_code = run_cli(env::args_os().collect());
    ExitCode::from(exit_code as u8)
}
