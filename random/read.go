package random

import (
	"fmt"
	"math/rand"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// ReadIOPS is to read randomly
func ReadIOPS() {
	var err error
	println("start RandomRead")
	baseRange := int64(1000000000)
	inputFile := "./dbsnp/1.txt"

	MaxIter := 100000

	f, err := os.Open(inputFile)
	check(err)

	for i := 0; i < MaxIter; i++ {
		// seek to pos
		posToSeek := rand.Int63n(baseRange)
		_, err = f.Seek(posToSeek, 0)
		check(err)

		// read bytes
		b := make([]byte, 5)
		_, err = f.Read(b)
		check(err)
	}
	println("stop RandomRead")
}

// ReadToMem is to test speed for memory loading
func ReadToMem() {
	println("read into memory")
	// try to read a chunk (1GB)
	chunkSize := int64(1024 * 1024 * 1024)

	inputFiles := []string{"./dbsnp/1.txt", "./dbsnp/2.txt", "./dbsnp/3.txt"}
	for _, inputFile := range inputFiles {
		f, err := os.Open(inputFile)
		check(err)

		// read into memory
		b := make([]byte, chunkSize)
		n, err := f.Read(b)
		fmt.Printf("memory loading done: %d bytes\n", n)
	}
	// inputFile := "./dbsnp/1.txt"
}
