package main

import (
	"bufio"
	"fmt"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type SnpKey struct {
	Chr  int16
	Pos  int32
	Refa []int16
	Refc []int16
	Refg []int16
	Reft []int16
	Alta []int16
	Altc []int16
	Altg []int16
	Altt []int16
}

type Snp map[SnpKey]string

func Read(inputTxt string) {
	file, err := os.Open(inputTxt)
	check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}

func main() {
	inputTxt := "./dbsnp/1.txt"
	fmt.Printf("hello!\n")
	read(inputTxt)
}
