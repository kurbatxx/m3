use m3u8_rs::Playlist;
use nom::IResult;
use std::io::Read;

fn main() {
    println!("Hello, world!");

    let mut file = std::fs::File::open("./src/python/index.m3u8").unwrap();
    let mut bytes: Vec<u8> = Vec::new();
    file.read_to_end(&mut bytes).unwrap();

    let parsed = m3u8_rs::parse_playlist(&bytes);

    let playlist = match parsed {
        Result::Ok((i, Playlist::MasterPlaylist(pl))) => println!("Master playlist:\n{:?}", pl),
        Result::Ok((i, Playlist::MediaPlaylist(pl))) => {
            //println!("Media playlist:\n{:?}", pl);
            //let key = pl.segments[1].clone().key.unwrap();
            let ts = pl.segments[1].clone().uri;

            println!("{}/{}", ts, ts);
            dbg!(pl.segments);
        }
        Result::Err(e) => panic!("Parsing error: \n{}", e),
    };
}
