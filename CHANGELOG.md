# CHANGELOG

<!-- version list -->

## v1.19.2 (2026-05-11)

### Bug Fixes

- **heatmap**: My previous commit broke the heatmap by storing images in the wrong format, this
  restores it.
  ([`f312bd5`](https://github.com/cse120-ucm/S26-CSE-324/commit/f312bd50187cf492fb230bba50d488f58919abd7))

### Code Style

- Added colors to the website (they're kinda ugly though)
  ([`3f7a570`](https://github.com/cse120-ucm/S26-CSE-324/commit/3f7a57081b9f26ce33d560df0da2369cb1c8f465))

- Changed logo to png, page colors, and added a white logo
  ([`37b2d6d`](https://github.com/cse120-ucm/S26-CSE-324/commit/37b2d6d7538d4870bfd3c59463aab36b3308acff))

- Changed primary background color
  ([`2501574`](https://github.com/cse120-ucm/S26-CSE-324/commit/25015746e217f21d52ec36ccd52f098cdc4a1a33))

### Refactoring

- Initial fix to image storage tests, and potential streamlit improvement to decrease load times
  ([`af5b573`](https://github.com/cse120-ucm/S26-CSE-324/commit/af5b573b666febb85aff2fdc908f46264afe61dc))


## v1.19.1 (2026-05-08)

### Bug Fixes

- Fixed broken test ([#179](https://github.com/cse120-ucm/S26-CSE-324/pull/179),
  [`16c56d8`](https://github.com/cse120-ucm/S26-CSE-324/commit/16c56d8bdc5654b316cc319f541c1cc2e75f6bfe))

- Switched to sending image bytesinstead of generating url to display image
  ([#179](https://github.com/cse120-ucm/S26-CSE-324/pull/179),
  [`16c56d8`](https://github.com/cse120-ucm/S26-CSE-324/commit/16c56d8bdc5654b316cc319f541c1cc2e75f6bfe))

- Switched to sending image bytesinstead of generating url to disp…
  ([#179](https://github.com/cse120-ucm/S26-CSE-324/pull/179),
  [`16c56d8`](https://github.com/cse120-ucm/S26-CSE-324/commit/16c56d8bdc5654b316cc319f541c1cc2e75f6bfe))


## v1.19.0 (2026-05-07)

### Bug Fixes

- Fixed flashing bug with heatmap ([#177](https://github.com/cse120-ucm/S26-CSE-324/pull/177),
  [`8678bc9`](https://github.com/cse120-ucm/S26-CSE-324/commit/8678bc9ce5685fe69bce0e30dfce8f089255b8e6))

- Resnet_liveprocessing now sends image to storage
  ([#177](https://github.com/cse120-ucm/S26-CSE-324/pull/177),
  [`8678bc9`](https://github.com/cse120-ucm/S26-CSE-324/commit/8678bc9ce5685fe69bce0e30dfce8f089255b8e6))

- **codespaces**: The feature is now compatible with codespaces, but the tests need to be cleaned up
  now ([#177](https://github.com/cse120-ucm/S26-CSE-324/pull/177),
  [`8678bc9`](https://github.com/cse120-ucm/S26-CSE-324/commit/8678bc9ce5685fe69bce0e30dfce8f089255b8e6))

### Features

- Added image preview to on-click popup in heatmap, fixed clipping issue with voronoi diagram
  ([#177](https://github.com/cse120-ucm/S26-CSE-324/pull/177),
  [`8678bc9`](https://github.com/cse120-ucm/S26-CSE-324/commit/8678bc9ce5685fe69bce0e30dfce8f089255b8e6))


## v1.18.0 (2026-05-07)

### Bug Fixes

- **delete**: I noticed the delete button was broken, so I fixed it
  ([`7f3bdd1`](https://github.com/cse120-ucm/S26-CSE-324/commit/7f3bdd1139a217c08fa9e494305852bfa4f0e070))

- **lint**: Code is now linted
  ([`1f30d01`](https://github.com/cse120-ucm/S26-CSE-324/commit/1f30d01e7847ad7108ff66305e08012f8d998174))

### Features

- **time**: Finalized UI and ran tests
  ([`5ace1cf`](https://github.com/cse120-ucm/S26-CSE-324/commit/5ace1cfe6dba1f17057b4f7e633f5ece21efdff3))

- **time**: Initial draft of adding times to ui, yet to be tested
  ([`c4f8e16`](https://github.com/cse120-ucm/S26-CSE-324/commit/c4f8e169a0f4753d7c111176a1cbf3068f82be90))

### Refactoring

- **frontend**: Added docstrings and comment to exportData.py and added instructions to
  Visualization HOW TO USE.md
  ([`e6453c5`](https://github.com/cse120-ucm/S26-CSE-324/commit/e6453c5aa17649afb37430cb556222e51785f482))

- **fullstack**: Used linter to check for any and all unused variables to maintain cleanliness
  ([`af2c007`](https://github.com/cse120-ucm/S26-CSE-324/commit/af2c007c3c8b235a95d0c28408501be292a1236b))

- **fullstack**: Used ruff check to look for unused variables
  ([`bf23ef6`](https://github.com/cse120-ucm/S26-CSE-324/commit/bf23ef6ac021a3f2e2504b0a8ce93077bac030f0))


## v1.17.0 (2026-05-06)

### Bug Fixes

- Removed running inference twice ([#174](https://github.com/cse120-ucm/S26-CSE-324/pull/174),
  [`4775290`](https://github.com/cse120-ucm/S26-CSE-324/commit/47752908e49a127fe2e2ca822d5517a1afe54307))

- Ui changes ([#174](https://github.com/cse120-ucm/S26-CSE-324/pull/174),
  [`4775290`](https://github.com/cse120-ucm/S26-CSE-324/commit/47752908e49a127fe2e2ca822d5517a1afe54307))

- **inference**: Updated tests and changed weights name
  ([#174](https://github.com/cse120-ucm/S26-CSE-324/pull/174),
  [`4775290`](https://github.com/cse120-ucm/S26-CSE-324/commit/47752908e49a127fe2e2ca822d5517a1afe54307))

### Features

- Added functionality to upload page, now sends to model to 'check' for response, if response good
  then allows upload to db ([#174](https://github.com/cse120-ucm/S26-CSE-324/pull/174),
  [`4775290`](https://github.com/cse120-ucm/S26-CSE-324/commit/47752908e49a127fe2e2ca822d5517a1afe54307))


## v1.16.0 (2026-05-06)

### Bug Fixes

- **frontend**: Fixed export data tests
  ([`119bb84`](https://github.com/cse120-ucm/S26-CSE-324/commit/119bb8484ecc60489e1659ab1357b679acfdc9f1))

- **frontend**: Fixed syntax errors in app.py and the cache misalignment in exportData.py
  ([`9c28f19`](https://github.com/cse120-ucm/S26-CSE-324/commit/9c28f197c634f0696fc45c31b009ca740f56e025))

- **tests**: Moved exportData code inside name = main loop to prevent code running on import. Moved
  database pytest fixture code to conftest so it runs one, because tests were terminating early.
  Reverted change to get df from db since it broke a test (might be better to update the test int
  the long run)
  ([`f77ff60`](https://github.com/cse120-ucm/S26-CSE-324/commit/f77ff60674ea61f66ec9a1ec48d5f087d22e346f))

### Features

- **frontend**: Added download button and dropdown menu for specific fields
  ([`9b8ef9d`](https://github.com/cse120-ucm/S26-CSE-324/commit/9b8ef9dfc53ad0300613ce49b6f92fa59b48f413))

### Refactoring

- **app**: Got rid of code that is no longer needed
  ([`68b7161`](https://github.com/cse120-ucm/S26-CSE-324/commit/68b7161852e60bb1d5a7dcfc054cd46bb834345a))

- **tabs**: Moved unused tabs to another folder
  ([`98afe6e`](https://github.com/cse120-ucm/S26-CSE-324/commit/98afe6e558bbef567e0233fa495a7e2d840fa74b))

- **tests**: Tested visualization pipeline
  ([`a6bf506`](https://github.com/cse120-ucm/S26-CSE-324/commit/a6bf5064100fd5082b296e89ab5c4698b98778d7))

- **UI**: Made more UI changes and got rid of commented out code for a cleaner look
  ([`7562272`](https://github.com/cse120-ucm/S26-CSE-324/commit/75622727d15a48c15d478224c425c47cf721cd05))

### Testing

- **Database**: Added test for database performance, which means pure throughput through sqlmodel
  ([`c1813a7`](https://github.com/cse120-ucm/S26-CSE-324/commit/c1813a78a59afa1928f86c5d7b95501288e659a9))


## v1.15.0 (2026-05-04)

### Bug Fixes

- **Database**: Corrected type mismatch in carrot metadata records
  ([`df4c6ea`](https://github.com/cse120-ucm/S26-CSE-324/commit/df4c6ea5dfae5e980569f20df0c7074c889867d0))

- **Database**: Fixed carrot metadata not retaining when field is loaded
  ([`5eea22a`](https://github.com/cse120-ucm/S26-CSE-324/commit/5eea22af629ea1231ebe29419b4f85abb866844c))

- **Tests**: Corrected tests broken by prior changes
  ([`bacd2fc`](https://github.com/cse120-ucm/S26-CSE-324/commit/bacd2fcace6a20dfe753b1d87c3b2d1a0dfa0038))

- **Visualization**: Added way to re-seed database with representative data
  ([`c218388`](https://github.com/cse120-ucm/S26-CSE-324/commit/c2183884fd9d83d3d97effbad1dbd5f7b3840a3a))

- **Visualization**: Fixed improper git diff
  ([`cea93a1`](https://github.com/cse120-ucm/S26-CSE-324/commit/cea93a15255d04a89f7bec537f668205375f9605))

### Documentation

- **Visualization**: Annotated and reorganized the field management page
  ([`ecd0d43`](https://github.com/cse120-ucm/S26-CSE-324/commit/ecd0d438fcc34ed3a1709b71c7d3a825ffc3a640))

- **Visualization**: Annotated heatmap page
  ([`7d79797`](https://github.com/cse120-ucm/S26-CSE-324/commit/7d7979744d80435e7537d832761fd911680862d1))

- **Visualization**: Update HOW TO USE
  ([`3bb8905`](https://github.com/cse120-ucm/S26-CSE-324/commit/3bb8905ba06c30dd7b1b1bda232970ac2a1e0d50))

### Features

- **Database**: Add new representative data to database seeding method
  ([`3057b0c`](https://github.com/cse120-ucm/S26-CSE-324/commit/3057b0c828f1ca8cf062d772a7e71c01deca3059))

- **Database**: Add representative dataset to seed database
  ([`df7f452`](https://github.com/cse120-ucm/S26-CSE-324/commit/df7f452fa09032a2b2d5eb52e6a4eb3899bf0253))

- **Visualization**: Add data poins feature group and toggle menu
  ([`39ff283`](https://github.com/cse120-ucm/S26-CSE-324/commit/39ff283e7b8f48426a77cdf070ea327971db1392))

- **Visualization**: Add heatmap to folium map
  ([`f252f17`](https://github.com/cse120-ucm/S26-CSE-324/commit/f252f17d1dfbd53b3bd4413828eb2854c3bd8888))

- **Visualization**: Add load from database to re-seed on command.
  ([`cb764ab`](https://github.com/cse120-ucm/S26-CSE-324/commit/cb764ab43c096642d90bf7e3889a007687cb4478))


## v1.14.2 (2026-05-02)

### Bug Fixes

- **render deploy**: Converted docker compose to render.yaml to allow it to use services
  ([`5b9bc68`](https://github.com/cse120-ucm/S26-CSE-324/commit/5b9bc68f4f42cd6265a5ff1cc23c3940da215e3b))


## v1.14.1 (2026-05-02)

### Bug Fixes

- **render**: Changed Dockerfile to find Streamlit port
  ([`1d4d844`](https://github.com/cse120-ucm/S26-CSE-324/commit/1d4d844ee4c90b85d489c33f5b08d2cd30f26bfd))


## v1.14.0 (2026-04-30)

### Bug Fixes

- Add_image_metadata now checks if point is within bounding box of field
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- Fixed tests not working ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- Fixed tests to reflect changes made to field data class
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- **image storage test**: Fixed image storage test to use new field boundaries
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- **image storage test**: Fixed unexpected issue with fix
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

### Features

- Added delete button to field creation page
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- Added new page to create field that can also display field; changed field data class to have 4
  corners as vertices instead of 2 points
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))

- Dropdown menu in heatmap view to select field, draws polygon around field
  ([#158](https://github.com/cse120-ucm/S26-CSE-324/pull/158),
  [`985e73a`](https://github.com/cse120-ucm/S26-CSE-324/commit/985e73ae763ee73ff4f9bb4018ef71981d73e7b6))


## v1.13.1 (2026-04-30)

### Bug Fixes

- **updating action**: Potential fix to get action working correctly
  ([`8535173`](https://github.com/cse120-ucm/S26-CSE-324/commit/8535173d5b23565d41c917f0eef64ef2332a378a))

### Refactoring

- **bucket storage**: Updated compose file to include MinIO, will check after commit
  ([`6649efc`](https://github.com/cse120-ucm/S26-CSE-324/commit/6649efc2989de23fb8875c3770e10ff866476cec))

- **image storage**: Added tests confirming that images are being stored in buckets, and retrieved
  correctly
  ([`57ebe6f`](https://github.com/cse120-ucm/S26-CSE-324/commit/57ebe6f165426660c2529b842885ccbbec74ae54))

- **image storage**: Changed image requester class to use buckets and presigned urls
  ([`59551f2`](https://github.com/cse120-ucm/S26-CSE-324/commit/59551f2e8d50a0ec4b3dc47df17ed425e7d2a897))

- **tests**: Updated code so that tests all pass correctly, and added safegaurd against dividing by
  0 in segmentation
  ([`ef0da89`](https://github.com/cse120-ucm/S26-CSE-324/commit/ef0da89a1d90708da9934861cd4dacd6956044ca))

- **updating action**: Updating the github workflow to accomodate MinIO
  ([`67561e0`](https://github.com/cse120-ucm/S26-CSE-324/commit/67561e0b3f40398815b984c5fc6c54b006f5c2d8))


## v1.13.0 (2026-04-29)

### Features

- **UI**: Made some changes to clean up the tabs
  ([`b354593`](https://github.com/cse120-ucm/S26-CSE-324/commit/b354593651516e64044a88b914ef96139a1d61c1))


## v1.12.0 (2026-04-18)

### Features

- **chore**: Added pytest.cov library and instructions on how to test coverage across src files,
  added pytest-cov to requirements.txt
  ([`1821b23`](https://github.com/cse120-ucm/S26-CSE-324/commit/1821b238774000626b56ca3a94f640307fccf328))

- **testing**: Added .coverage file
  ([`e60d38b`](https://github.com/cse120-ucm/S26-CSE-324/commit/e60d38b0f9545f88a69a1cc8bf4be1658d516909))


## v1.11.0 (2026-04-18)

### Bug Fixes

- **image_storage**: Directories are now nested and field names are sanitized before storage. Also
  changed how images are named to prevent duplicates
  ([`bf3519a`](https://github.com/cse120-ucm/S26-CSE-324/commit/bf3519a79a18bd443a3b1e9327a727d6611e0566))

### Features

- **image_storage**: Created a first draft of image storage, need to test
  ([`620a6aa`](https://github.com/cse120-ucm/S26-CSE-324/commit/620a6aa08ec21d97ee13adc8f11e2157009b0a69))

### Testing

- **image_storage**: Image storage has been tested, and appears to be all good
  ([`a4bb2a1`](https://github.com/cse120-ucm/S26-CSE-324/commit/a4bb2a10d775f68d8fa38a5caae5514f322bc32a))


## v1.10.0 (2026-04-18)

### Features

- **testing**: Created baisc tests for streamlit app
  ([`7b2cd10`](https://github.com/cse120-ucm/S26-CSE-324/commit/7b2cd108312a03c073e6f7dba6661af1406aeafe))

### Testing

- **streamlit**: Added test for switching between pages
  ([`47508a1`](https://github.com/cse120-ucm/S26-CSE-324/commit/47508a16d0fe511c5e9e67e51d3f4aed2c5415e1))

- **streamlit**: Refactored dataUplaod page in order to pass image uploading test
  ([`43df138`](https://github.com/cse120-ucm/S26-CSE-324/commit/43df13851deefe8841111ed784c28a2c78a1dd04))


## v1.9.0 (2026-04-18)

### Bug Fixes

- Renamed integration test to be covered by pytest
  ([`8ca517d`](https://github.com/cse120-ucm/S26-CSE-324/commit/8ca517d43a002b21dc7b9c222410285b30e0a1e3))

### Features

- **testing**: Added test images for segmentation and resnet tests
  ([`f09e42d`](https://github.com/cse120-ucm/S26-CSE-324/commit/f09e42dee72baa9adb9622b6fd03f2a00b7c6ad0))

- **tests**: Added metadata for representative images
  ([`9369464`](https://github.com/cse120-ucm/S26-CSE-324/commit/9369464bdbbb3d717a1d0663791aeeb2ab8bf115))

### Testing

- Add integration test for live processing
  ([`7eb5522`](https://github.com/cse120-ucm/S26-CSE-324/commit/7eb55221354f6510c8a17d5f288dad47b8150959))

- Reworked inference unit tests to use dummy weights instead of relying on pth file
  ([`ed558b4`](https://github.com/cse120-ucm/S26-CSE-324/commit/ed558b4c2a88dfbfaf2cc788cf958e56e12b496f))

- Reworked segmentation test to use representative images
  ([`b906dae`](https://github.com/cse120-ucm/S26-CSE-324/commit/b906daed2e3142ff5fa02de70d6f96c606bb24f3))


## v1.8.0 (2026-04-18)

### Documentation

- **resnet**: Added docstrings
  ([`c8c8950`](https://github.com/cse120-ucm/S26-CSE-324/commit/c8c8950d06745346370a98aae1e0602b05d0273c))

- **resnet**: Added some comments
  ([`66be2da`](https://github.com/cse120-ucm/S26-CSE-324/commit/66be2da389947357b5e18598ffe40a9382b08451))

### Features

- **inference**: Added arbitrary inference
  ([`168c180`](https://github.com/cse120-ucm/S26-CSE-324/commit/168c1804815032f76a9ac93fea2382f2a4f87cde))

### Refactoring

- **resnet**: Changed normalization information to be collected dynamically, rather than hard coded
  ([`e189202`](https://github.com/cse120-ucm/S26-CSE-324/commit/e189202e58c4b67d41412190aa069d87f1fc802a))

- **resnet**: Changed weights to be stored in data/Outputs to be consistent with the file structure
  ([`fe1e505`](https://github.com/cse120-ucm/S26-CSE-324/commit/fe1e505492422bea7431aa847950c2d4cc56eb29))

- **resnet**: Removed blank image handling from hot loop, and improved docstrings
  ([`89ef38a`](https://github.com/cse120-ucm/S26-CSE-324/commit/89ef38add9095b7187a61476f575872cdafdf01f))

- **resnet**: Tried to improve model by using augmented data, not seeing significant improvement.
  next step is to clean up the file
  ([`b2c4036`](https://github.com/cse120-ucm/S26-CSE-324/commit/b2c4036ba202aab3d4c9c5b35094b9601c098d23))


## v1.7.0 (2026-04-15)

### Bug Fixes

- Issues with tests ([#146](https://github.com/cse120-ucm/S26-CSE-324/pull/146),
  [`b46b74f`](https://github.com/cse120-ucm/S26-CSE-324/commit/b46b74f6a290608347a9c68c154a145b33baa96d))

### Continuous Integration

- **requirements**: Added torch and torchvision to requirements
  ([#146](https://github.com/cse120-ucm/S26-CSE-324/pull/146),
  [`b46b74f`](https://github.com/cse120-ucm/S26-CSE-324/commit/b46b74f6a290608347a9c68c154a145b33baa96d))

### Features

- Added running inference on pretrained resnet model, as well as resnet_liveprocessing to combine
  segmentation & resnet inference to one pipeline + sending to database
  ([#146](https://github.com/cse120-ucm/S26-CSE-324/pull/146),
  [`b46b74f`](https://github.com/cse120-ucm/S26-CSE-324/commit/b46b74f6a290608347a9c68c154a145b33baa96d))


## v1.6.0 (2026-04-04)

### Bug Fixes

- **Models**: Renamed rclone instance to "box" from "remote" to remove ambiguity
  ([`36a9717`](https://github.com/cse120-ucm/S26-CSE-324/commit/36a97179005acf07cee81d790dadf8b37181b46c))

### Features

- **Models**: Add color segmentation logic
  ([`856494d`](https://github.com/cse120-ucm/S26-CSE-324/commit/856494d2693d730d09c98a3f744143890cb6664f))

- **Models**: Add color-based segmentation visualization
  ([`21c0c5a`](https://github.com/cse120-ucm/S26-CSE-324/commit/21c0c5a95e994959049a88076350092bbaedbff3))

- **Models**: Add model output and manual verification steps
  ([`0477f36`](https://github.com/cse120-ucm/S26-CSE-324/commit/0477f364f28b8fa512fe973c1318c3239154a438))

- **Models**: Add verbose output for debug
  ([`27215a9`](https://github.com/cse120-ucm/S26-CSE-324/commit/27215a96ffbee1c8529e8cd87721044b8f8d7b40))

- **Models**: Added upload to box functionality
  ([`a6a20a2`](https://github.com/cse120-ucm/S26-CSE-324/commit/a6a20a2695338f40d32badae7e920c9f56cb7a13))


## v1.5.0 (2026-04-04)

### Bug Fixes

- Release now configured for closed PRs
  ([`6206b9e`](https://github.com/cse120-ucm/S26-CSE-324/commit/6206b9ec62c9371ba61f3d25815a3c14cf1f80ea))

- **cd**: Corrected syntax in release.yml for manual release dispatch
  ([`99c9405`](https://github.com/cse120-ucm/S26-CSE-324/commit/99c94051a8f10c7211814041d7831071dfdd4f8f))

- **cd**: Syntax error and github-script updated to v8 node 24 runtime
  ([`78deb52`](https://github.com/cse120-ucm/S26-CSE-324/commit/78deb526efe0ae2d20ad508fab3bb7266fb8ef2c))

- **ci**: Updated test.yml to private CSE120 cluster
  ([`768bd81`](https://github.com/cse120-ucm/S26-CSE-324/commit/768bd81d2b050a0605fb9013bce78ab1a5427116))

### Features

- Updated ci/cd to private cluster
  ([`c505a6f`](https://github.com/cse120-ucm/S26-CSE-324/commit/c505a6fb9d270ec2fa47c0f6b3e61bff7d604159))


## v1.4.0 (2026-04-03)

### Bug Fixes

- Changed carrotmodel.predict to not create new appended image automatically
  ([#131](https://github.com/cse120-ucm/S26-CSE-324/pull/131),
  [`75d3d8a`](https://github.com/cse120-ucm/S26-CSE-324/commit/75d3d8a82674e2a5f1de4f76d04aba6c2b72b8e8))

- Minor bug in using model.draw ([#131](https://github.com/cse120-ucm/S26-CSE-324/pull/131),
  [`75d3d8a`](https://github.com/cse120-ucm/S26-CSE-324/commit/75d3d8a82674e2a5f1de4f76d04aba6c2b72b8e8))

- **Models**: Add info on how to resolve expired tokens
  ([`5776b5c`](https://github.com/cse120-ucm/S26-CSE-324/commit/5776b5c3104ebc857da5a51bf4eea549a96c140e))

- **Models**: Changed rclone config file write to be readable
  ([`4e4f7c5`](https://github.com/cse120-ucm/S26-CSE-324/commit/4e4f7c54c38ecc5f60470456968609355e15ff41))

- **Models**: Moved torch from requirements to manual install due to large package size
  ([`070a2bd`](https://github.com/cse120-ucm/S26-CSE-324/commit/070a2bdb53ad4c044a36e3f75fb4aa0a651865e6))

- **YOLO**: Liveprocessing->database interface completed and tested
  ([`d4ad184`](https://github.com/cse120-ucm/S26-CSE-324/commit/d4ad1840d6e82fea2495448f54a66d7385244b03))

### Documentation

- **Models**: Revised manual verification steps
  ([`966a98a`](https://github.com/cse120-ucm/S26-CSE-324/commit/966a98a6208415a3006bada167f3c26b56d87f1b))

- **Models**: Update HOW TO USE with preliminaries
  ([`60f4e7b`](https://github.com/cse120-ucm/S26-CSE-324/commit/60f4e7bcb53d94744a0d93d6767fe96ec2874e76))

### Features

- **Models**: Add automatic rclone setup procedure
  ([`03a6fb7`](https://github.com/cse120-ucm/S26-CSE-324/commit/03a6fb76e9690fae773f545fbde8285603c9460c))

- **Models**: Add dataset loader utility
  ([`18c7d80`](https://github.com/cse120-ucm/S26-CSE-324/commit/18c7d80da6f82efdf041b63e7879d6c4821c92ea))

- **Models**: Added rclone manual setup instructions
  ([`b97e6e6`](https://github.com/cse120-ucm/S26-CSE-324/commit/b97e6e627b72d87773c9785ff04be933fc75adc2))

- **YOLO**: Liveprocessing->database interface created, test file created. Waiting for
  database_requester class to be merged to main for final refactor/bugfix
  ([`3b0086c`](https://github.com/cse120-ucm/S26-CSE-324/commit/3b0086c92342cdaf8f57b9ed0d1c57ec8ae70c55))


## v1.3.0 (2026-03-21)

### Documentation

- Update README.md
  ([`052bf09`](https://github.com/cse120-ucm/S26-CSE-324/commit/052bf0993972e0dc305fdaa88385cecdd80e0918))

### Features

- **database**: Finished integrating database into visualization with barebones test
  ([`d7fcac4`](https://github.com/cse120-ucm/S26-CSE-324/commit/d7fcac41fd6148b138122ac576f8e1daef38c836))

- **database**: Implement high level visualization data retrieval
  ([`4c77622`](https://github.com/cse120-ucm/S26-CSE-324/commit/4c7762287825e19fc71820e8027fbb78c378e0a4))

- **dataupload**: Fixed file upload text
  ([`9fd097f`](https://github.com/cse120-ucm/S26-CSE-324/commit/9fd097f1483073a38c55301e0134921345c86fe9))

- **dataupload**: Fixed minor caption issues
  ([`c2472e1`](https://github.com/cse120-ucm/S26-CSE-324/commit/c2472e1e25a18cfeae798ebaa845795c3d839cdc))

- **features**: Added data uplaoding and deleting feature as well as fixed logo image issues
  ([`a2b43a5`](https://github.com/cse120-ucm/S26-CSE-324/commit/a2b43a55e7932c0079a9a5f454c02905e43c0f2e))

- **features**: Fixed a minor error with the file upload
  ([`cdfd1bf`](https://github.com/cse120-ucm/S26-CSE-324/commit/cdfd1bfb4c696c24173d4dd3b44de72845784e04))

- **vision model**: Adds trained yolov7 model in onnx format and required framework to run model
  ([`fd14dcd`](https://github.com/cse120-ucm/S26-CSE-324/commit/fd14dcd887ffe4d1bb63184d665435c0775ba753))

- **YOLO**: Added new liveprocessing class to bridge between Streamlit, the model, and the database.
  Also tested it.
  ([`c7990e9`](https://github.com/cse120-ucm/S26-CSE-324/commit/c7990e914dccd08b8f456764205d35bca1ced000))

### Refactoring

- **database**: Moved models.py to Database folder and updated database.model calls accordingly
  ([`457fec3`](https://github.com/cse120-ucm/S26-CSE-324/commit/457fec35b8f1a94e65043abe03b39eb3a0dae7e2))


## v1.2.0 (2026-03-19)

### Documentation

- Added steel thread baseline docs for visualization app
  ([`a0a32b9`](https://github.com/cse120-ucm/S26-CSE-324/commit/a0a32b928bbbf766db2e7126fba88ce043d01cf8))

- **visualization**: Updated HOW TO USE to reflect refactor
  ([`78c035a`](https://github.com/cse120-ucm/S26-CSE-324/commit/78c035aac167217775d718d6f423d675acc3449d))

### Features

- **visualization**: Add basic skeleton of major functionality
  ([`970fda6`](https://github.com/cse120-ucm/S26-CSE-324/commit/970fda6ca535c44a8d1780aee6c6a9c4551a2f68))

- **visualization**: Add dataframe classes and database request call
  ([`6289582`](https://github.com/cse120-ucm/S26-CSE-324/commit/6289582fd56bb9ea596aeb2c8a4085bcd15c40ac))

- **visualization**: Add devcontainer and setup script
  ([`af03e73`](https://github.com/cse120-ucm/S26-CSE-324/commit/af03e73f0e4615b66bbe402520a91e3377e2366b))

- **visualization**: Add preliminary page layout
  ([`65e95ad`](https://github.com/cse120-ucm/S26-CSE-324/commit/65e95ad555db20a3aa7a45df9ed3889f02610aed))

- **visualization**: Updated import requirements
  ([`1d898ff`](https://github.com/cse120-ucm/S26-CSE-324/commit/1d898ffea7dcd4e28ab561b46ce58b452b42fb50))

- **visualization app**: Added preliminaries
  ([`15e0956`](https://github.com/cse120-ucm/S26-CSE-324/commit/15e0956553fd9770d937b606ad3cc19a05c5d63e))

- **visualization data**: Add table and histogram plot with representative data
  ([`662c8e8`](https://github.com/cse120-ucm/S26-CSE-324/commit/662c8e864d76de059e7d29a3898ccd101f0f6bf9))

- **visualization data pipeline**: Ported representative data from code exploration, created test
  file
  ([`01c7108`](https://github.com/cse120-ucm/S26-CSE-324/commit/01c7108099b5fe3c8a006447e48261ab08247026))

### Refactoring

- **visualization**: Readjust file structure into src and test
  ([`619ae6b`](https://github.com/cse120-ucm/S26-CSE-324/commit/619ae6bb192b81ac3bbccbe0fa29147560f80b72))


## v1.1.0 (2026-03-19)

### Bug Fixes

- Fixed another bad import
  ([`6684519`](https://github.com/cse120-ucm/S26-CSE-324/commit/66845192d1cda2f8ecf7fa56dd3c67d9419afd17))

- Fixed imports in source
  ([`077981e`](https://github.com/cse120-ucm/S26-CSE-324/commit/077981e7bab2b7ad55fcfa884906818a00bc3b3d))

- Fixed lazy import also being broken...
  ([`629e5d0`](https://github.com/cse120-ucm/S26-CSE-324/commit/629e5d01e8b9469ffe735f5baa714e615a1bd827))

- Updated test file imports not seeing Model folder in source
  ([`5eecca3`](https://github.com/cse120-ucm/S26-CSE-324/commit/5eecca35ace5426e04a3295ff284b7352a09efff))

- Updated test.yml to run module-scope pytest
  ([`0f658b6`](https://github.com/cse120-ucm/S26-CSE-324/commit/0f658b62b5829f759f86ea8d701c7d162ee13e61))

### Features

- Add preliminary "how to use" files
  ([`3c1980d`](https://github.com/cse120-ucm/S26-CSE-324/commit/3c1980d5457f793fe5304bd0c87f0c07fda260b3))

- Add source file structure
  ([`aaeabc4`](https://github.com/cse120-ucm/S26-CSE-324/commit/aaeabc491d22f3551e79ae4adb4a003b0f7525ce))

### Refactoring

- Fix import of source files in DB tests
  ([`c2513b8`](https://github.com/cse120-ucm/S26-CSE-324/commit/c2513b891e425edefb763a89bd1f7fbe98bae538))

- Move database files into database folder
  ([`e6369e4`](https://github.com/cse120-ucm/S26-CSE-324/commit/e6369e40419d28cdfd4dfee4c7ddc28cbdece089))

- Move DB tests into tests/Database
  ([`ff1ab67`](https://github.com/cse120-ucm/S26-CSE-324/commit/ff1ab67641da2f9473046e9a87be1350fe60b336))

- Move models to source folder
  ([`2f63149`](https://github.com/cse120-ucm/S26-CSE-324/commit/2f631499eaf6de550f7ca6c8aad8e5662afe0824))


## v1.0.0 (2026-03-18)

- Initial Release
