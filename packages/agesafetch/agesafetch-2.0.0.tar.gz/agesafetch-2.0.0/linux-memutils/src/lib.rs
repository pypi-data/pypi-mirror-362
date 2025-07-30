// SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
// SPDX-License-Identifier: MIT
/*!
This crate provides basic utilities for reading from physical memory on Linux.

It is developed in tandem with the [`agesafetch`] CLI crate, but its features
may also come in handy for other use cases.

[`agesafetch`]: https://crates.io/crates/agesafetch
*/
pub mod agesa;
pub mod iomem;
pub mod reader;
