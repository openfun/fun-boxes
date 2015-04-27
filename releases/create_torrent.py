#!/usr/bin/env python
import argparse
import os
import libtorrent

# Those are all public trackers sampled from
# https://gist.github.com/mcandre/eab4166938ed4205bef4
TRACKERS = [
    "udp://tracker.openbittorrent.com:80",
    "udp://tracker.publicbt.com:80",
    "udp://tracker.istole.it:80",
    "udp://tracker.btzoo.eu:80/announce",
    "http://opensharing.org:2710/announce",
    "udp://open.demonii.com:1337/announce",
    "http://announce.torrentsmd.com:8080/announce.php",
    "http://announce.torrentsmd.com:6969/announce",
    "http://bt.careland.com.cn:6969/announce",
    "http://i.bandito.org/announce",
    "http://bttrack.9you.com/announce"
]


def main():
    parser = argparse.ArgumentParser(description="Create a .torrent file for distributing OpenFUN releases")
    parser.add_argument("-o", "--output", help="Output torrent file. Defaults to '<input_file.box>.torrent'.")
    parser.add_argument("input", help="Path to .box file")
    args = parser.parse_args()

    output_path = args.output or args.input + ".torrent"
    create_torrent(args.input, output_path)

def create_torrent(input_path, output_path):
    input_path = os.path.abspath(input_path)
    input_dir = os.path.dirname(input_path)
    input_file_name = os.path.basename(input_path)
    output_path = os.path.abspath(output_path)

    fs = libtorrent.file_storage()
    file_size = os.path.getsize(input_path)
    fs.add_file(input_file_name, file_size)

    torrent = libtorrent.create_torrent(fs)
    torrent.set_creator("OpenFUN http://github.com/openfun/")
    for tracker in TRACKERS:
        torrent.add_tracker(tracker)
    libtorrent.set_piece_hashes(torrent, input_dir)

    with open(output_path, 'wb') as f:
        f.write(libtorrent.bencode(torrent.generate()))

if __name__ == "__main__":
    main()
