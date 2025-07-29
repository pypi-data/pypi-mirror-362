[![Build Status](https://app.travis-ci.com/hasii2011/peskytm.svg?branch=master)](https://app.travis-ci.com/hasii2011/pyut2xml)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Introduction

This utility is an update to a [blog post](https://hsanchezii.wordpress.com/2022/04/12/manually-verify-time-machine-snapshots/) that aimed to help OS X users verify external Time Machine disks and overcome a diskutil deficiency. 

# Rationale

The blog entry notes that a user can use the graphical Disk Utility in a certain order to unmount the Time Machine volume and then use the utility to "*Repair*" the volume.

Unfortunately, even after unmounting the volume OS X leaves what I think are local snapshots mounted that reference the external volume.  They are of the form:

`com.apple.TimeMachine.2021-08-31-103804.backup@/dev/disk7s2 on /Volumes/ . . . . . . .`



Thus, the Repair operation fails.



This utility manually unmounts those *pesky* time machine volumes



```
Usage
peskytm --help
Usage: peskytm.py [OPTIONS]

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

```

Notice this utility has no parameters.  You simply execute it.  Internally, `peskytm` use `sudo`, so you will be prompted for your OS X password (Don't worry the utility does nothing but pass it along).  You will then see output like the following:



`peskytm`

`com.apple.TimeMachine.2021-08-31-103804.backup@/dev/disk7s2 unmounted`
`com.apple.TimeMachine.2021-09-09-221954.backup@/dev/disk7s2 unmounted`
`com.apple.TimeMachine.2021-09-16-141610.backup@/dev/disk7s2 unmounted`
`com.apple.TimeMachine.2021-09-26-120444.backup@/dev/disk7s2 unmounted`
`com.apple.TimeMachine.2021-10-06-172708.backup@/dev/disk7s2 unmounted`
`com.apple.TimeMachine.2021-10-14-144954.backup@/dev/disk7s2 unmounted`



Once you manually unmount this pesky volumes you can either use the graphical utility or the command line utility (CLI).  An example, usage of the CLI is:



`sudo fsck_apfs -y /dev/disk7s2`



# How to Install

`pipx install peskytm`

