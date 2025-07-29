package main

import (
	"C"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"

	"github.com/jinzhu/copier"
	rpmdb "github.com/knqyf263/go-rpmdb/pkg"

	_ "github.com/glebarez/go-sqlite"
)

type packageInfo struct {
	Name            string
	Version         string
	Release         string
	Arch            string
	SourceRpm       string
	Size            int
	License         string
	Vendor          string
	Modularitylabel string
	Summary         string
	PGP             string
	SigMD5          string
	InstallTime     int
	BaseNames       []string
	DirIndexes      []int32
	DirNames        []string
	FileSizes       []int32
	FileDigests     []string
	FileModes       []uint16
	FileFlags       []int32
	UserNames       []string
	GroupNames      []string

	Provides []string
	Requires []string
}

//export getrpmdbInfo
func getrpmdbInfo(fileNameIn *C.char) *C.char {
	return C.CString(getrpmdbInfodInfoInternal(C.GoString(fileNameIn)))
}

func main() {
	//getrpmdbInfo(C.CString("/home/mike/pyrpmdb/test-data/centos5-plain-Packages"))
	//getrpmdbInfo(C.CString("/home/mike/pyrpmdb/test-data/cbl-mariner-2.0-rpmdb.sqlite"))
}

func getrpmdbInfodInfoInternal(fileName string) string {
	var (
		rpmdbPkg *packageInfo
	)
	returnValue := "{ \"error\" : \"Unknown\" }"
	db, err := rpmdb.Open(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf("{ \"error\": \"path error:%v\" }", fileName)
		} else {
			returnValue = fmt.Sprintf("{ \"error\": \"%s: %v\"}", fileName, err)
		}
	} else {
		pkgList, err := db.ListPackages()
		if err != nil {
			returnValue = fmt.Sprintf("{ \"error\": \"%s: %v\"}", fileName, err)
		} else {
			mySlice := []packageInfo{}
			for _, pkg := range pkgList {
				rpmdbPkg = new(packageInfo)
				copier.Copy(rpmdbPkg, *pkg)
				mySlice = append(
					mySlice,
					*rpmdbPkg)
			}
			data, _ := json.Marshal(mySlice)
			returnValue = string(data)
		}
	}
	// fmt.Printf("%s\n", returnValue)
	return returnValue
}
