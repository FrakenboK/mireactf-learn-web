package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/flag", handleFlag)
	fmt.Println("Starting server on port 1337...")
	log.Fatal(http.ListenAndServe(":1337", nil))
}

func handleFlag(w http.ResponseWriter, r *http.Request) {
	authHeader := r.Header.Get("Authorization")
	if authHeader != "Bearer MireactfG00000000l" {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	flag := os.Getenv("FLAG")
	if flag == "" {
		http.Error(w, "FLAG environment variable not set", http.StatusInternalServerError)
		return
	}

	fmt.Fprintln(w, flag)
}
