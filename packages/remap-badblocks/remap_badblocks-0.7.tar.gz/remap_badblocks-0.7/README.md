# remap\_badblocks

`remap_badblocks` is a Linux utility that lets you safely create a virtual block device which skips bad sectors and transparently remaps new bad sectors to healthy spare sectors elsewhere on the same disk. It is useful for squeezing safe, stable usage out of partially failing disks.

## 🔧 How It Works

* Stores devices configurations in a persistent database (this is crucial for accessing the remapped disks)
  * badblocks
  * mapping between real and virtual blocks
  * number of spare sectors in the device
* It can either create a new mapping from scratch or update the existing one to remap new badblocks by keeping everything intact
* It can generate device-mapper devices that follow the stored mappings

## 🚀 Usage

```bash
remap-badblocks [-h] [-P DB_PATH] {add,get,update,apply} ...
```

### Global Options

* `-P, --db-path` — path to the configuration database (default is internal)

### Commands:

#### `add`

Register a new device in the remap database.

```bash
remap-badblocks add [--wwn WWN] [--path PATH] name
```

* `name`: required alias for the device
* `--wwn`: optional WWN of the device
* `--path`: optional device path (e.g., `/dev/sdX`)

#### `get`

Retrieve registered devices or a specific one:

```bash
remap-badblocks get [--id ID]
```

#### `update`

Compute and store badblocks, update the mapping:

```bash
remap-badblocks update [--mode {read,write,skip}] [--block-range RANGE] [--output OUTPUT] [--spare-space N] id
```

* `--mode`: how badblocks should operate (default: `read`)
* `--block-range`: e.g., `0-100000` or `1573-`
* `--output`: also save badblocks to a file
* `--spare-space`: reserve N good sectors for future remapping

#### `apply`

Apply the device-mapper table to create a virtual remapped device:

```bash
remap-badblocks apply [--id ID] [--method device-mapper]
```

## 🛠️ Example Workflow

1. Register the device:

```bash
remap-badblocks add --path /dev/disk/by-id/myid mydrive
```

2. Run badblocks scan and create the mapping:

```bash
remap-badblocks update --mode read --spare-space 512MB --id 1
```

3. Apply the remapping to create a safe virtual block device:

```bash
remap-badblocks apply --id 1
```

4. Use `/dev/mapper/mydrive` as your new clean device

## ⚠️ Warnings

* This tool **does not recover corrupted data**, it only prevents future reads/writes from known bad sectors.
* Only usable on non-boot drives.
* Always keep backups.
* Devices are not persistent between boots, you have to manually apply them at startup (`remap-badblocks apply`), but this will be changed in the future.

## 📆 Future Plans

### Done
- [x] Manage dependencies between different devices
- [x] Empty db column for "apply at startup"
- [x] Leave free space in disks for possible future metadata (around 4-8B per badblock + 12-24B per mapping, let's consider around 1k badblocks + 1k mappings = 16-32kB => maybe 100kB is good)
- [x] Check already applied devices
- [x] Add version option for getting version

## 🤝 Contributions Welcome

Feel free to submit improvements or suggestions.

For issues or feature requests, please [open a card on GitLab](https://gitlab.com/Luigi-98/remap_badblocks/-/issues).
