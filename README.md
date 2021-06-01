# dns-timing

# Introduction

This repo contains a few scripts to collect DNS lookup-times, aggregate the times to average times, infer some statistics about the times collected and create DNS lookup workload traces.

These scripts were used to create DNS workload traces with access times and gater statistics on the collected times, which was used for simulations in the "Boosting cache performance using access times". (add link)

# Requirements

The dns-timing.py scripts use bind for the DNS lookups cache, specifically it uses the dig command. **You must have bind installed on your system to run this script**.

Also the following python external libraries are being used:
* pause
* matplotlib
* numpy

you can use the requirments file to install the required libraries.

Just run the following:
```bash
pip install -r requirments.txt
```

# Usage

In case this is the first time you use this repo, the general workflow is:
1. Choose your urls to time, we used the 1M_webrank.
2. Run dns-timing.py on how many vms you wish to use, we used 6, running on the chosen urls from (1). you may also choose the number of iterations to time all the urls, including delays between iterations.
3. After the times were collected you can use find-invalid.py, which finds suspected urls for being invalid, and you can make a new filtered urls list file.
4. Now you can use trace-maker.py using either the filtered or the un-filtered urls + the times collected.
5. You can also gather some statistics on the times collected using timing-stats.py

This was our general workflow creating our workloads traces.

All scripts has --help or -h flag to get usage of the script.

Examples of getting usage and flags info below,

```bash
> python dns-timing.py -h
> usage: dns-timing.py [-h] [-input INPUT] [-dd D] [-hd H] max_vm vm iters

Collects dns lookup times for cache miss and hit from list of urls.

positional arguments:
  max_vm        a positive integer for the max number of vms.
  vm            an integer for the vm number.
  iters         number of iterations to run the script over the segment of
                urls.

optional arguments:
  -h, --help    show this help message and exit
  -input INPUT  path to input file containing urls to time (default:
                "1M_webrank").
  -dd D         an integer for the iteration delay in days (default: 1).
  -hd H         an integer for the iteration delay in hours (default: 1).
```

```bash
> python timing-stats.py -h
> usage: timing-stats.py [-h] [-basedir BASEDIR] [-vm_num VM_NUM]
                       [-o OUTPUT_PATH] [-i INPUT_PATH] [--logscale]

Displays statistics about times collected

optional arguments:
  -h, --help        show this help message and exit
  -basedir BASEDIR  path to base directory containing collected times
                    (default: "data").
  -vm_num VM_NUM    a positive integer for the used number of vms.
  -i INPUT_PATH     path for aggregated times input file, if not given
                    aggregation is done from files in basedir.
  --logscale        flag to make histogram plot y-scale be in log-scale.
```

```bash
> python find-invalid.py -h
> usage: usage: find-invalid.py [-h] [-filename FILENAME] [-basedir BASEDIR]

Displays suspect urls from file that might be invalid and creates a new urls
list file on demand.

optional arguments:
  -h, --help          show this help message and exit
  -filename FILENAME  path to input file containing urls to time (default:
                      "1M_webrank").
  -basedir BASEDIR    path to base directory containing collected times
                      (default: ".").
```

```bash
> python trace-maker.py -h
> usage: trace-maker.py [-h] [-input INPUT] [-length L] [-num N]
                      [-vm_num VM_NUM] [-basedir BASEDIR] [-r_hit R_HIT]
                      [-r_miss R_MISS] [--replace]

Creates new random traces from input file

optional arguments:
  -h, --help        show this help message and exit
  -input INPUT      path to input file containing urls to time (default:
                    "filtered_1M_webrank").
  -length L         an integer for the number of requests in trace (default:
                    5e7).
  -num N            an integer for the number of traces to create (default:
                    1).
  -vm_num VM_NUM    a positive integer for the used number of vms.
  -basedir BASEDIR  path to base directory containing collected times
                    (default: "data").
  -r_hit R_HIT      value for hit time in case of replace=True and negative
                    time found (default: 1000).
  -r_miss R_MISS    value for miss time in case of replace=True and negative
                    time found (default: 10000).
  --replace         if this flag is used then negative times will be replaced.
```

# Our data

All of the available data files for this repo can be found [here](https://drive.google.com/drive/folders/1znXAK1suZzmg0aJ3HzRMrykIAXRIyrBu?usp=sharing).

**Times collected from BGU**
* [December 31st 2019 - January 19th 2019](https://drive.google.com/drive/folders/1iPBfbX5WaUCeWmFdHEuM-xrmcM-CSYYB?usp=sharing)
* [May 6th 2020 - June 5th 2020](https://drive.google.com/drive/folders/1i2CofHd_gwsH6it4dvjKsU7rSKr9DFJP?usp=sharing)

**Average times files**
* [dns.times](https://drive.google.com/file/d/1gE3F-M4jQtmN_Nue8KnXFW0Y1V0PxcDc/view?usp=sharing)
* [poc_dns7.times](https://drive.google.com/file/d/1YKZvOafSJOxo43roPbIATgFvhBPu_UGc/view?usp=sharing)
* [poc_dns11.times](https://drive.google.com/file/d/1WTpLfJE8maXHgZ9uI5XhdZ4giFNhyiiS/view?usp=sharing)
* [mean_times.out](https://drive.google.com/file/d/1Hc5XogvvN_w7eZkWSILSVFk-Bun1ykTo/view?usp=sharing)

<!-- # Further reading
* Boosting Cache Performance byAccess Time Awareness
* mp-traces - Another traces maker repo used in this paper to create traces for latency aware cache policies simulations. -->
