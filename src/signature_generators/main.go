package main

import (
    "fmt"
    "log"
    "os"
    b "github.com/dgryski/go-bitstream"
)

func main() {

    path1 := os.Args[1]
    path2 := os.Args[2]
    fmt.Println(path1)
    fmt.Println(path2)

    file, err := os.Open(path1)
    if err != nil {
        log.Fatal("Error while opening file", err)
    }

    defer file.Close()

    fmt.Printf("%s opened\n", path1)

	br := b.NewReader(file)

    
    // Skip the following data:
	// - NumOfSpatial Regions: (32 bits) only 1 supported
	// - SpatialLocationFlag: (1 bit) always the whole image
	// - PixelX_1: (16 bits) always 0
	// - PixelY_1: (16 bits) always 0
	skipBits1, _ := br.ReadBits(32 + 1 + 16 + 16)

    // width - 1, and height - 1
	// PixelX_2: (16 bits) is width - 1
	// PixelY_2: (16 bits) is height - 1
    width, _ := br.ReadBits(16)
    height, _ := br.ReadBits(16)
    width++
    height++

    // StartFrameOfSpatialRegion, always 0
    startFrameOfSpatialRegion, _ := br.ReadBits(32)

    // NumOfFrames
	// it's the number of fine signatures
    lastIndex, _ := br.ReadBits(32)

    // MediaTimeUnit
    timeBaseDenominator, _ := br.ReadBits(16)
    var timeBaseNumerator = 1

    // Skip the following data
	// - MediaTimeFlagOfSpatialRegion: (1 bit) always 1
	// - StartMediaTimeOfSpatialRegion: (32 bits) always 0
    skipBits2, _ := br.ReadBits(1 + 32)

    // EndMediaTimeOfSpatialRegion
    lastCoarsePts, _ := br.ReadBits(32)

	// Coarse signatures
	// numOfSegments = number of coarse signatures
	numOfSegments, _ := br.ReadBits(32)

    fmt.Printf("Skipped data:\n%+v\n", skipBits1)
    fmt.Printf("W:\n%+v\n", width)
    fmt.Printf("H:\n%+v\n", height)
    fmt.Printf("Start frame:\n%+v\n", startFrameOfSpatialRegion)
    fmt.Printf("Last index:\n%+v\n", lastIndex)
    fmt.Printf("Time base den:\n%+v\n", timeBaseDenominator)
    fmt.Printf("Time base num:\n%+v\n", timeBaseNumerator)
    fmt.Printf("Skipped data:\n%+v\n", skipBits2)
    fmt.Printf("Last coarse signature PTS(ms):\n%+v\n", lastCoarsePts)
    fmt.Printf("Number of segments:\n%+v\n", numOfSegments)

}
