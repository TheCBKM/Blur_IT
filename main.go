package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"

	shell "github.com/ipfs/go-ipfs-api"
	uuid "github.com/satori/go.uuid"
)

func main() {
	http.HandleFunc("/", foo)

	http.ListenAndServe(":5000", nil)
}

func foo(w http.ResponseWriter, req *http.Request) {
	var s string
	if req.Method == http.MethodPost {

		// open
		f, h, err := req.FormFile("q")
		iferrw(w, err)

		defer f.Close()

		// for your information
		// fmt.Println("\nfile:", f, "\nheader:", h, "\nerr", err)

		// read
		bs, err := ioutil.ReadAll(f)
		iferrw(w, err)
		extension := filepath.Ext(h.Filename)
		filename, _ := uuid.NewV4()
		dst, err := os.Create(filepath.Join("./", filename.String()+extension))
		iferrw(w, err)

		defer dst.Close()

		_, err = dst.Write(bs)
		x := filename.String()
		_ = runBlur(x+extension, "out"+x+extension)
		s = upload(w, "out"+x+extension)

	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, `<form method="POST"  enctype="multipart/form-data">
    <label for="idx-f">Choose File To Upload</label>
    <input type="file" id="idx-f" name="q">
    <br>
    <input type="submit">
</form>`+s)
}

func runBlur(src string, dst string) string {
	fmt.Println("Run Blur")
	dir, _ := os.Getwd()
	fmt.Println(dir)
	cmd := exec.Command("python", dir+"/"+"faceblur.py", dir+"/"+src, dir+"/"+dst)
	fmt.Println(cmd)
	stdoutStderr, err := cmd.CombinedOutput()
	iferr(err)
	fmt.Printf("%s\n", stdoutStderr)
	return string(stdoutStderr)
}

func upload(w http.ResponseWriter, src string) string {
	sh := shell.NewShell("https://ipfs.infura.io:5001")
	f, err := os.Open(src)
	iferrw(w, err)

	cid, err := sh.Add(f)
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s", err)
		os.Exit(1)
	}
	fmt.Printf("added %s", cid)
	s := `<a target="_blank" href="https://ipfs.io/ipfs/` + cid + `">link</a>
	<br>
	<img  src="https://ipfs.io/ipfs/` + cid + `">link</img>`
	return s
}

func iferr(err error) {
	if err != nil {
		log.Fatal(err)
	}

}
func iferrw(w http.ResponseWriter, err error) {
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

}
