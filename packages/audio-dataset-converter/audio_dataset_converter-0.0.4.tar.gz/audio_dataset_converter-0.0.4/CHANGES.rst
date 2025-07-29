Changelog
=========

0.0.4 (2025-07-15)
------------------

- requiring seppl>=0.2.20 now for improved help requests in `adc-convert` tool


0.0.3 (2025-07-10)
------------------

- added `set-placeholder` filter for dynamically setting (temporary) placeholders at runtime
- added `--resume_from` option to relevant readers that allows resuming the data processing
  from the first file that matches this glob expression (e.g., `*/012345.wav`)
- requiring seppl>=0.2.17 now for resume, split group, skippable plugin support and avoiding deprecated use of pkg_resources
- `to-adams-sp` writer now uses `-t` short flag for the transcript like the `from-adams-sp` reader
- added the `from-multi` meta-reader that combines multiple base readers and returns their output
- added the `to-multi` meta-writer that forwards the data to multiple base writers
- using `wai_common` instead of `wai.common` now
- added `split_group` parameter to splittable writers (stream/batch)
- fixed the construction of the error messages in the pyfunc reader/filter/writer classes
- added `metadata-to-placeholder` filter to transfer meta-data files into placeholders


0.0.2 (2025-03-14)
------------------

- added `setuptools` as dependency
- switched to underscores in project name
- added `discard-by-name` filter
- requiring seppl>=0.2.13 now
- added support for aliases
- added placeholder support to tools: `adc-convert`, `adc-exec`
- added placeholder support to readers: `from-adams-ac`, `from-subdir-ac`, `from-txt-ac`, `from-adams-sp`,
  `from-commonvoice-sp`, `from-festvox-sp`, `from-hf-audiofolder-sp`, `from-txt-sp`, `from-data`, `poll-dir`,
  `from-pyfunc`
- added placeholder support to writers: `to-adams-ac`, `to-subdir-ac`, `to-txt-ac`, `to-adams-sp`, `to-commonvoice-sp`,
  `to-festvox-sp`, `to-hf-audiofolder-sp`, `to-txt-sp`, `to-audioinfo`, `to-data`


0.0.1 (2024-07-05)
------------------

- initial release

