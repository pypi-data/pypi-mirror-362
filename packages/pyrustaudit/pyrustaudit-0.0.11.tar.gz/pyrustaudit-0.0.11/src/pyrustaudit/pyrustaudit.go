package main

import (
	"C"
	"encoding/json"
	"errors"
	"fmt"
	rustaudit "github.com/rust-secure-code/go-rustaudit"
	"os"
	"path/filepath"
)

//export getrustAudit
func getrustAudit(fileNameIn *C.char) *C.char {
	return C.CString(getrustAuditInternal(C.GoString(fileNameIn)))
}

func main() {
	//getrpmdbInfo(C.CString("/home/mike/pyrustaudit/test-data/centos5-plain-Packages"))
	//getrpmdbInfo(C.CString("/home/mike/pyrustaudit/test-data/cbl-mariner-2.0-rpmdb.sqlite"))
}

func getrustAuditInternal(fileName string) string {
	returnValue := "{ \"error\" : \"Unknown\" }"

	r, err := os.Open(fileName)
	if err != nil {
		if pathErr := (*os.PathError)(nil); errors.As(err, &pathErr) && filepath.Clean(pathErr.Path) == filepath.Clean(fileName) {
			returnValue = fmt.Sprintf("{ \"error\": \"path error:%v\" }", fileName)
		} else {
			returnValue = fmt.Sprintf("{ \"error\": \"%s: %v\"}", fileName, err)
		}
	} else {
		pkgList, err := rustaudit.GetDependencyInfo(r)
		r.Close()
		if err != nil {
			returnValue = fmt.Sprintf("{ \"error\": \"%s: %v\"}", fileName, err)
		} else {
			data, _ := json.Marshal(pkgList)
			returnValue = string(data)
		}
	}
	// fmt.Printf("%s\n", returnValue)
	return returnValue
}
