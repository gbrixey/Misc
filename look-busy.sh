#!/bin/bash

# Font styles
REGULAR=$(tput sgr0)
BOLD=$(tput bold)

# Font colors
BLACK=$(tput setaf 0)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
GREEN=$(tput setaf 2)
CYAN=$(tput setaf 6)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)

# Prints the first argument and a newline and sleeps
# for a number of seconds determined by the second argument
print_wait () {
    printf "$1\n"
    sleep $2
}

###########################################################
# PROGRESS BAR FUNCTIONS
###########################################################

# Prints one line of a progress bar.
# Pass in a percent and a time to sleep.
progress_bar () {
    printf "\r${BOLD}[${GREEN}"
    local PROGRESS=$(((40 * $1) / 100))
    local SPACES=$((40 - $PROGRESS))
    printf "%${PROGRESS}s" | tr " " "="
    printf %${SPACES}s
    printf "${BLACK}] ($1%%)${REGULAR}  "
    sleep $2
}

# Erase progress bar and print first argument.
progress_bar_done () {
    printf "\r%-50s\n" "$1"
}

# Fast progress bar
progress_bar_fast () {
    # Vary the numbers slightly.
    local OPTION=$((RANDOM % 4))
    local i=0
    if [ $OPTION -eq 0 ]
        then
        for i in {0,4,11,37,60,91}; do
            progress_bar $i 0.2
        done
    elif [ $OPTION -eq 1 ]
        then
        for i in {0,12,21,29,46,77}; do
            progress_bar $i 0.2
        done
    elif [ $OPTION -eq 2 ]
        then
        for i in {5,20,36,62,80,96}; do
            progress_bar $i 0.2
        done
    elif [ $OPTION -eq 3 ]
        then
        for i in {2,19,34,50,63,89}; do
            progress_bar $i 0.2
        done
    fi
    progress_bar 100 0.2
}

# Slow progress bar
progress_bar_slow () {
    local PROGRESS=0
    while true
    do
        local STEP=$((RANDOM % 7 + 2))
        PROGRESS=$((PROGRESS + STEP))
        if [ $PROGRESS -lt 100 ]
            then
            progress_bar $PROGRESS 0.4
        else
            progress_bar 100 0.4
            return
        fi
    done
}

# Progress bar that starts quickly but finishes slowly
progress_bar_slow_finish () {
    # Get to a high percentage quickly
    local PROGRESS=0
    local i=0
    for (( i = 0; i < 4; i++ )); do
        local JUMP=$((RANDOM % 3 + 21))
        PROGRESS=$((PROGRESS + JUMP))
        progress_bar $PROGRESS 0.4
    done
    # Creep slowly toward 100%
    sleep 0.6
    PROGRESS=$((PROGRESS + 3))
    progress_bar $PROGRESS 1
    PROGRESS=$((PROGRESS + 2))
    progress_bar $PROGRESS 1
    while [ $PROGRESS -lt 99 ]
    do
        PROGRESS=$((PROGRESS + 1))
        progress_bar $PROGRESS 1
    done
    progress_bar 100 0.4
}

# Progress bar that starts slow and suddenly finishes
progress_bar_sudden_finish () {
    local PROGRESS=3
    local i=0
    for (( i = 0; i < 5; i++ )); do
        local STEP=$((RANDOM % 5 + 5))
        PROGRESS=$((PROGRESS + STEP))
        progress_bar $PROGRESS 1
    done
    PROGRESS=$((RANDOM % 10 + 84))
    progress_bar $PROGRESS 0.4
    progress_bar 100 0.4
}

# Progress bar that gets about halfway finished and then goes backwards
progress_bar_backwards () {
    local PROGRESS=0
    local i=0
    for (( i = 0; i < 6; i++ )); do
        local STEP=$((RANDOM % 5 + 8))
        PROGRESS=$((PROGRESS + STEP))
        progress_bar $PROGRESS 0.4
    done
    PROGRESS=$((PROGRESS + 1))
    progress_bar $PROGRESS 0.4
    PROGRESS=$((PROGRESS - 3))
    progress_bar $PROGRESS 0.4
    PROGRESS=$((PROGRESS - 5))
    progress_bar $PROGRESS 0.4
    while [ $PROGRESS -gt 0 ]
    do
        local STEP=$((RANDOM % 8 + 10))
        PROGRESS=$((PROGRESS - STEP))
        if [[ $PROGRESS -lt 5 ]]
        then
            PROGRESS=0
        fi
        progress_bar $PROGRESS 0.4
    done
}

###########################################################
# OTHER ANIMATED STUFF
###########################################################

# Prints the first argument and an animated ellipsis
# for an integer number of seconds determined by the second argument.
# Prints the third argument after the ellipsis on completion.
ellipsis () {
    local ITERATIONS=$(($2 * 5))
    local i=0
    for (( i = 0; i < $ITERATIONS; i++ )); do
        if [ $((i % 3)) -eq 0 ]
            then
            printf "\r$1.  "
        elif [ $((i % 3)) -eq 1 ]
            then
            printf "\r$1.. "
        else
            printf "\r$1..."
        fi
        sleep 0.2
    done
    printf "\r$1... $3\n"
}

# Animates a spinner for a number of seconds
# determined by the first argument.
spinner () {
    local ITERATIONS=$(($1 * 10))
    local i=0
    for (( i = 0; i < $ITERATIONS; i++ )); do
        if [ $((i % 4)) -eq 0 ]
            then
            printf "\r-"
        elif [ $((i % 4)) -eq 1 ]
            then
            printf "\r\\"
        elif [ $((i % 4)) -eq 2 ]
            then
            printf "\r|"
        elif [ $((i % 4)) -eq 3 ]
            then
            printf "\r/"
        fi
        sleep 0.1
    done
    printf "\r \r"
}

###########################################################
# FAKE ACTIVITIES
###########################################################

download_and_extract_file () {
    print_wait "Resource path found." 0.1
    ellipsis "Connecting" 5 "Done"
    print_wait "${BOLD}Downloading https://gamm.com/linux/misc/potrzebie.tar.gz${REGULAR}" 0.1
    progress_bar_slow
    progress_bar_done "Download complete (${BOLD}2.6 MB${REGULAR})                        "
    print_wait "Validating archive..." 0.4
    print_wait "${YELLOW}No checksum for downloaded archive, recording checksum in user configuration.${BLACK}" 0.1
    print_wait "tar -xzf potrzebie.tar.gz\n" 1.2
}

spider () {
    local CHOICE=$((RANDOM % 2))
    if [ $CHOICE -eq 0 ]
    then
        print_wait "wget --spider http://gamm.com/ptJVNr/basement.html" 0.1
        print_wait "Spider mode enabled. Check if remote file exists." 0.1
        print_wait "HTTP request sent, awaiting response... ${BOLD}${GREEN}200 OK${REGULAR}${BLACK}" 0.1
        print_wait "Length: 1206 (1.2K) [text/html]" 0.1
        print_wait "Remote file exists. Spider found in file.\n" 0.1
    else
        print_wait "wget --spider http://gamm.com/ght2v1/attic.html" 0.1
        print_wait "Spider mode enabled. Check if remote file exists." 0.1
        print_wait "HTTP request sent, awaiting response... ${BOLD}${RED}404 Not Found${REGULAR}${BLACK}" 0.1
        print_wait "Remote file not found. No spiders found.\n" 0.1
    fi
}

office_space () {
    local REPORTS=$((RANDOM % 15 + 8))
    print_wait "Performing DNS lookups for TPS reports..." 0.1
    progress_bar_slow_finish
    progress_bar_done "$REPORTS reports found. (${BOLD}8.1 MB${REGULAR})                           "
    ellipsis "Printing reports" 4 ""
    printf "${RED}${BOLD}Exception${BLACK}${REGULAR} in thread \"main\" java.io.${RED}${BOLD}PCLoadLetterException${BLACK}${REGULAR}\n"
    printf "    at java.io.PrintStream.print(Native Method)\n"
    printf "    at com.initech.util.ReportPrinter.print(ReportPrinter.java:105)\n"
    printf "    at com.initech.util.ReportPrinter.startInternal(ReportPrinter.java:51)\n"
    printf "    at com.initech.util.DocumentManager.complete(DocumentManager.java:212)\n"
    printf "    at com.initech.util.DocumentManager.yeah(DocumentManager.java:753)\n"
    printf "    at org.apache.poi.openxml4j.opc.OPCPackage.open(OPCPackage.java:273)\n"
    printf "    at org.apache.poi.util.PackageHelper.open(PackageHelper.java:37)\n"
    printf "    at org.apache.poi.xssf.usermodel.XSSFWorkbook.<init>(XSSFWorkbook.java:273)\n"
    printf "    ... 170 more\n\n"
    sleep 3
}

finger () {
    print_wait "w" 0.1
    printf "10:05:34 up 5 days, 23:55,  6 users,  load average: 2.02, 1.39, 1.15\n"
    printf "USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU  WHAT\n"
    printf "glenb    tty1     -                Tue18    4days  0.37s  0.33s -bash\n"
    printf "glenb    :0       :0               Sat19   ?xdm?   2:54m  2.68s upstart --user\n"
    printf "glenb    pts/10   :0               10:00    5:01   0.21s 52.37s gnome-terminal\n"
    printf "glenb    pts/16   :0               07:04    2.00s  0.18s 52.37s gnome-terminal\n"
    printf "glenb    pts/14   :0               07:02   46:42   0.29s 52.37s gnome-terminal\n"
    printf "freddy   pts/11   :0               10:00    3:29   0.12s 52.37s -bash\n\n"
    spinner 4
    print_wait "finger freddy" 0.1
    printf "${BOLD}[${BLUE}expert.gamm.com${BLACK}]${REGULAR}\n"
    printf "Login: ${BOLD}freddy${REGULAR}                   Name: ${BOLD}Frederick Brody${REGULAR}\n"
    printf "Directory: /home/usr/freddy     Shell: /bin/bash\n"
    printf "Last login Tue Jul 17 15:21 on ttyQ7 from ${BOLD}${BLUE}mitten.gamm.com${REGULAR}${BLACK}\n"
    printf "${BOLD}Unread mail since ${BLUE}Wed Jul 11 13:00:54${BLACK}${REGULAR}\n"
    printf "No Plan.\n\n"
}

postgresql () {
    print_wait "Trying to pronounce PostgreSQL..." 0.1
    spinner 4
    printf "${RED}${BOLD}Aborted.${BLACK}${REGULAR}"
    printf "\nA fatal error has been detected by the Java Runtime Environment:\n"
    printf "SIGSEGV (0xb) at pc=0x00002aaaaaf6d9c3, pid=2185, tid=1086892352\n"
    printf "JRE version: 6.0_21-b06\n"
    printf "Java VM: Java HotSpot(TM) 64-Bit Server VM (17.0-b16 mixed martial arts linux-amd64)\n\n"
}

space_requirements () {
    print_wait "Exporting environment variables from project settings:" 1.5
    print_wait "    ${BOLD}${MAGENTA}DELIVER_PASSWORD${REGULAR}${BLACK}" 0.1
    print_wait "    ${BOLD}${MAGENTA}DELIVER_USER${REGULAR}${BLACK}" 1.0
    print_wait "Computing space requirements..." 0.1
    progress_bar_sudden_finish
    progress_bar_done "Done"
    print_wait "${BOLD}Extracting source cache${REGULAR}" 0.1
    progress_bar_sudden_finish
    progress_bar_done "Done"
    sleep 1
    printf "${RED}${BOLD}Exception${BLACK}${REGULAR} in thread \"main\" java.lang.${RED}${BOLD}NullPointerException${BLACK}${REGULAR}\n"
    printf "    at com.gamm.webservices.adapters.ResultAdapter.load(ResultAdapter.java:272)\n"
    printf "    at com.gamm.webservices.adapters.MasterAdapter.main(MasterAdapter.java:25)\n"
    printf "    at org.apache.catalina.core.StandardContext.listenerStart(StandardContext.java:4738)\n"
    printf "    at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5181)\n"
    printf "    at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:150)\n"
    printf "    at org.apache.catalina.core.ContainerBase.addChildInternal(ContainerBase.java:725)\n"
    printf "    at org.apache.catalina.core.ContainerBase.addChild(ContainerBase.java:701)\n"
    printf "    at org.apache.catalina.core.StandardHost.addChild(StandardHost.java:717)\n"
    printf "    at org.apache.catalina.startup.HostConfig.deployDescriptor(HostConfig.java:586)\n"
    printf "    at org.apache.catalina.startup.HostConfig$DeployDescriptor.run(HostConfig.java:1780)\n"
    printf "    at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)\n"
    printf "    at java.util.concurrent.FutureTask.run(FutureTask.java:266)\n"
    printf "    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)\n"
    printf "    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)\n"
    printf "    ... 19 more\n"
}

unknown_option () {
    ellipsis "Starting tractor" 1 ""
    print_wait "tractor -ws --use-root --please" 0.1
    print_wait "Operation succeeded with warnings (1):\n" 0.1
    print_wait "${BOLD}${YELLOW}Warning${BLACK}${REGULAR}: tractor ignored unknown option --please" 0.1
    print_wait "Try 'tractor --help' for more information." 2
}

registers () {
    print_wait "Starting Norman Antibacteria" 0.1
    ellipsis "Authorizing" 3 "Done"
    ellipsis "Scanning directory /usr/local/gamm/beep" 3
    print_wait "${GREEN}${BOLD}0 bacteria found${REGULAR}${BLACK}." 0.1
    print_wait "Saved log in /Users/glenb/Library/Logs/Norman/bacteria.log" 0.1
    print_wait "\n${BLUE}${BOLD}Registers:${BLACK}${REGULAR}" 0.1
    print_wait "RAX=0x34372e302e3095e1, RBX=0x00002aaaae39dcd0," 0.1
    print_wait "RCX=0x0000000000000000, RDX=0x0000000000000000," 0.1
    print_wait "RSP=0x0000000040c89870, RBP=0x0000000040c898c0," 0.1
    print_wait "RSI=0x0000000040c898e8, RDI=0x000000004fd139c8," 0.1
    print_wait "R8 =0x000000004fb631f0, R9 =0x000000004faf5d30," 0.1
    print_wait "R10=0x00002aaaaaf6d999, R11=0x00002b1243b39580," 0.1
    print_wait "R12=0x00002aaaae3706d0, R13=0x00002aaaae39dcd0," 0.1
    print_wait "R14=0x0000000040c898e8, R15=0x000000004fd13800," 0.1
    print_wait "RIP=0x00002aaaaaf6d9c3, EFL=0x0000000000010202," 0.1
    print_wait "CSGSFS=0x0000000000000033," 0.1
    print_wait "ERR=0x0000000000000000\n" 2
}

osx_warning () {
    print_wait "${BOLD}${YELLOW}Warning${BLACK}${REGULAR}: You are using OS X 10.12." 3
}

install_and_remove_dependencies () {
    print_wait "brew install mackinac" 0.2
    print_wait "${BOLD}${GREEN}==>${BLACK} Installing dependencies for mackinac: ${GREEN}libffi, libressl, libmetalink, glib${BLACK}${REGULAR}" 0.1

    print_wait "${BOLD}${GREEN}==>${BLACK} Installing mackinac dependency: ${GREEN}libffi${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading https://mirrorservice.org/sites/sources.redhat.com/pub/libffi/libffi-3.0.13.tar.gz${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} ./configure --prefix=/usr/local/Cellar/libffi/3.0.13${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} make install${REGULAR}" 2.2
    print_wait "${BOLD}${BLUE}==>${BLACK} Summary${REGULAR}" 0.1
    print_wait "🍺  /usr/local/Cellar/libffi/3.0.13: 14 files, 360.4K, built in 13 seconds" 0.1

    print_wait "${BOLD}${GREEN}==>${BLACK} Installing mackinac dependency: ${GREEN}libressl${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-2.3.2.tar.gz${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} ./configure --disable-silent-rules --prefix=/usr/local/Cellar/libressl/2.3.2 --with-openssldir=/usr/local/etc/libressl --sysconfdir=/${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} make${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make check${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make install${REGULAR}" 2
    print_wait "${BOLD}${BLUE}==>${BLACK} Summary${REGULAR}" 0.1
    print_wait "🍺  /usr/local/Cellar/libressl/2.3.2: 375 files, 8.1M, built in 1 minute 18 seconds" 0.1

    print_wait "${BOLD}${GREEN}==>${BLACK} Installing mackinac dependency: ${GREEN}libmetalink${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading https://launchpad.net/libmetalink/trunk/libmetalink-0.1.3/+download/libmetalink-0.1.3.tar.xz${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading from https://launchpadlibrarian.net/210087595/libmetalink-0.1.3.tar.xz${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} ./configure --prefix=/usr/local/Cellar/libmetalink/0.1.3${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} make install${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} Summary${REGULAR}" 0.1
    print_wait "🍺  /usr/local/Cellar/libmetalink/0.1.3: 29 files, 176.1K, built in 12 seconds" 0.1

    print_wait "${BOLD}${GREEN}==>${BLACK} Installing mackinac dependency: ${GREEN}glib${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading from http://ftp.cse.buffalo.edu/pub/Gnome/sources/glib/2.46/glib-2.46.2.tar.xz${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading https://raw.githubusercontent.com/Homebrew/patches/59e4d32/glib/hardcoded-paths.diff${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading https://raw.githubusercontent.com/Homebrew/patches/59e4d32/glib/gio.patch${REGULAR}" 0.1
    progress_bar_fast
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} Patching${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} Applying hardcoded-paths.diff${REGULAR}" 1
    print_wait "patching file gio/gdbusprivate.c" 1
    print_wait "Hunk #1 succeeded at 2068 (offset -31 lines)." 0.1
    print_wait "Hunk #2 succeeded at 2078 (offset -31 lines)." 0.1
    print_wait "patching file gio/xdgmime/xdgmime.c" 1
    print_wait "patching file glib/gutils.c" 1
    print_wait "Hunk #1 succeeded at 1940 (offset 2 lines)." 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Applying gio.patch${REGULAR}" 0.1
    print_wait "patching file gio/Makefile.am" 1
    print_wait "Hunk #2 succeeded at 525 (offset 9 lines)." 0.1
    print_wait "patching file gio/Makefile.in" 1
    print_wait "Hunk #1 succeeded at 162 (offset 29 lines)." 0.1
    print_wait "Hunk #2 succeeded at 188 (offset 28 lines)." 0.1
    print_wait "Hunk #3 succeeded at 334 (offset 31 lines)." 0.1
    print_wait "Hunk #4 succeeded at 3590 (offset 154 lines)." 0.1
    print_wait "Hunk #5 succeeded at business without really trying." 0.1
    print_wait "patching file gio/Makefile.am" 1
    print_wait "patching file gio/Makefile.in" 1
    print_wait "Hunk #1 succeeded at 177 (offset -4 lines)." 0.1
    print_wait "Hunk #2 succeeded at 311 (offset -4 lines)." 0.1
    print_wait "Hunk #3 succeeded at 3317 (offset -5 lines)." 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} ./configure --disable-maintainer-mode --disable-silent-rules --disable-dtrace --disable-libelf --enable-static${REGULAR}" 0.5
    print_wait "${BOLD}${BLUE}==>${BLACK} make${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make install${REGULAR}" 1
    print_wait "🍺  /usr/local/Cellar/glib/2.46.2: 429 files, 22.6M, built in 1 minute 54 seconds" 0.1

    printf "\n"
    ellipsis "Reconsidering dependencies" 6 ""
    print_wait "${BOLD}${GREEN}==>${BLACK} Removing unnecessary dependencies: ${GREEN}libffi, libressl, libmetalink${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${GREEN}==>${BLACK} Removing dependency: ${GREEN}libffi${BLACK}${REGULAR}" 0.1
    progress_bar_fast
    progress_bar_done "Done"
    print_wait "${BOLD}${GREEN}==>${BLACK} Removing dependency: ${GREEN}libressl${BLACK}${REGULAR}" 0.1
    progress_bar_fast
    progress_bar_done "Done"
    print_wait "${BOLD}${GREEN}==>${BLACK} Removing dependency: ${GREEN}libmetalink${BLACK}${REGULAR}" 0.1
    progress_bar_fast
    progress_bar_done "Done"

    printf "\n"
    print_wait "${BOLD}${GREEN}==>${BLACK} Installing ${GREEN}mackinac${BLACK}${REGULAR}" 0.1
    print_wait "${BOLD}${BLUE}==>${BLACK} Downloading from https://www.gamm.com/etc/mackinac/mackinac-1.17.1.tar.xz${REGULAR}" 0.1
    progress_bar_slow
    printf "\n"
    print_wait "${BOLD}${BLUE}==>${BLACK} ./configure --prefix=/usr/local/Cellar/mackinac/1.17.1 --sysconfdir=/usr/local/etc --with-bot --with-proxy --enable-ipv6 --enable-true-c${REGULAR}" 0.5
    print_wait "config.status: creating src/Makefile" 0.2
    print_wait "config.status: creating src/Makemakefilefile" 0.3
    print_wait "config.status: creating src/Makemakemakefilefilefile" 0.4
    print_wait "${BOLD}${BLUE}==>${BLACK} make make make${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make make${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make${REGULAR}" 1
    print_wait "${BOLD}${BLUE}==>${BLACK} make install${REGULAR}" 1
    print_wait "🍺  /usr/local/Cellar/mackinac/1.17.1: 125439 files, 365M, built in 2 seconds" 0.1
}

certificate_request () {
    print_wait "Creating certificate request" 0.1
    progress_bar_fast
    progress_bar_done "Done"
    print_wait "Generating p12 files" 0.1
    spinner 2
    print_wait "Done" 0.5
    print_wait "Generating provisioning profiles" 0.1
    progress_bar_fast
    progress_bar_done "Created com.gamm.mackinac.adhoc.mobileprovision"
    progress_bar_fast
    progress_bar_done "Created com.gamm.mackinac.appstore.mobileprovision"
    progress_bar_fast
    progress_bar_done "Created com.gamm.mackinac.enterprise.mobileprovision"
    progress_bar_fast
    progress_bar_done "Created com.gamm.mackinac.development.mobileprovision"
    print_wait "Done" 1.5
}

mta_schedule () {
    print_wait "curl -nqrw https://gamm.com/mta/schedule.rtf > /dev/null 2>&1" 0.8
}

print_random_numbers () {
    print_wait "Printing numbers to terminal..." 0.1
    local ROWS=$((RANDOM % 8 + 9))
    local COLS=$((RANDOM % 3 + 3))
    local i=0
    for (( i = 0; i < $ROWS; i++ )); do
        for (( j = 0; j < $COLS; j++ )); do
            printf $(((RANDOM + RANDOM + RANDOM) * 10000000000 + (RANDOM + RANDOM + RANDOM) * 100000 + (RANDOM + RANDOM + RANDOM)))
            printf " "
            sleep 0.2
        done
        printf "\n"
    done
}

encryption () {
    print_wait "Encryption unsuccessful, retrying..." 0.1
    spinner 3
    print_wait "curl -s --ciphers rot13 https://gamm.com/misc/caesar > caesar.log" 0.5
    progress_bar_fast
    progress_bar_done "Encryption complete"
}

timing_function () {
    local BUILD_ARTIFACTS=$((RANDOM % 154 + 2))
    print_wait "Collecting $BUILD_ARTIFACTS build artifacts..." 1.1
    print_wait "${CYAN}/usr/bin/xcrun /opt/rubies/ruby-2.3.1/lib/ruby/gems/2.3.0/gems/gym-1.11.3/lib/assets/wrap_xcodebuild/xcbuild-safe.sh -exportArchive -exportOptionsPlist '/var/folders/jm/fw86rxds0xn69sk40d18y69m0000gp/T/gym_config20161116-4007-1ue7r9y.plist' -archivePath /Users/distiller/Library/Developer/Xcode/Archives/2016-11-16/gamm-mackinac-1.17.0\ 2016-11-16\ 09.01.17.xcarchive -exportPath '/var/folders/jm/fw86rxds0xn69sk40d18y69m0000gp/T/gym_output20161116-4007-qx5mhj'${BLACK}" 0.1
    print_wait "Smoothing timing functions..." 0.1
    progress_bar_slow
    print_wait "\nDone" 0.1
}

autosave () {
    local NUM_FILES=$((RANDOM % 20 + 3))
    print_wait "Detected ${BLUE}${BOLD}$NUM_FILES${REGULAR}${BLACK} autosave files from previous session." 0.5
    print_wait "Attempting recovery..." 0.1
    progress_bar_backwards
    progress_bar_done "${RED}${BOLD}Failed.${REGULAR}${BLACK}                                            "
    sleep 1
    print_wait "bash: help: command not found" 1.5
    print_wait "Sweeping up broken jars..." 0.1
    progress_bar_fast
    progress_bar_done "Done"
}

###########################################################
# MAIN LOOP
###########################################################

startup () {
    print_wait "${BLUE}${BOLD}Starting node${BLACK}${REGULAR}" 0.5
    print_wait "${BOLD}Applying container tweaks${REGULAR}" 0.4
    print_wait "Add containers to ~/.ssh/config as node0" 0.1
    print_wait "Server certificate: ${BOLD}${MAGENTA}*.s3.amazonaws.com${BLACK}${REGULAR}" 0.1
    print_wait "Server certificate: ${BOLD}${MAGENTA}DigiCert Baltimore CA-2 G2${BLACK}${REGULAR}" 0.1
    print_wait "Server certificate: ${BOLD}${MAGENTA}Baltimore CyberTrust Root${BLACK}${REGULAR}" 0.1
    print_wait "Setting environment variables" 1.5
    print_wait "    ${CYAN}${BOLD}GAMM_ARTIFACTS${BLACK}${REGULAR}=/tmp/gamm/artifacts.alot" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_BRANCH${BLACK}${REGULAR}=master" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_BUILD_IMAGE${BLACK}${REGULAR}=osx" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_COMPARE${BLACK}${REGULAR}=github" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_NODE_INDEX${BLACK}${REGULAR}=0" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_SHA1${BLACK}${REGULAR}=e1788dc523b161f4a659e7070ff15bba7f4ebc2f" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_TESTS${BLACK}${REGULAR}=false" 0.1
    print_wait "    ${CYAN}${BOLD}GAMM_USERNAME${BLACK}${REGULAR}=glenb" 0.1
    ellipsis "Summoning inference daemon" 4 ""
    print_wait "Inference daemon summoned." 0.1
    print_wait "Testing progress bar..." 0.5
    progress_bar_slow
    progress_bar_done "Done"
}

main_loop () {
    clear
    printf "${BLACK}"
    while true
    do
        startup
        osx_warning
        unknown_option
        autosave
        download_and_extract_file
        encryption
        spider
        office_space
        finger
        registers
        certificate_request
        space_requirements
        postgresql
        mta_schedule
        print_random_numbers
        timing_function
        install_and_remove_dependencies
    done
}

main_loop