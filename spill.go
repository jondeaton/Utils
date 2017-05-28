// spil.go
// This program spills the contents of a directory

package main

import (
	"fmt"
	"Flag"
	"os"
	"io/ioutil"
)


func main() {

	spilled := flag.String("directory", "", "spill `directory`")
	destination := flag.String("destination", "", )


	files, _ = := ioutil.ReadDir(spilled)
	
	// Loop through all files
	for _, f := range files {
		os.Rename()
	}

}