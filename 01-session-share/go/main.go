package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	token, _ := r.Cookie("token")
	expiration := time.Now()
	expiration = expiration.AddDate(1, 0, 0)
	cookie := http.Cookie{Name: "token", Value: "setNewToken", Expires: expiration}
	http.SetCookie(w, &cookie)
	fmt.Fprintf(w, "Cookie token: %s", token)
}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
