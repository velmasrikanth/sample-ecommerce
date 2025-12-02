package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"
)

var (
	ordersMu sync.Mutex
	orders   = make(map[int]Order)
	nextID   = 1
)

type Order struct {
	ID        int       `json:"id"`
	UserID    int       `json:"user_id"`
	ProductID int       `json:"product_id"`
	Quantity  int       `json:"quantity"`
	CreatedAt time.Time `json:"created_at"`
}

func main() {
	host := "0.0.0.0"
	port := os.Getenv("PORT")
	if port == "" {
		port = "5003"
	}
	addr := host + ":" + port

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	http.HandleFunc("/orders", ordersHandler)

	log.Printf("Order service listening on %s\n", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}

func ordersHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		listOrders(w, r)
		return
	}
	if r.Method == "POST" {
		createOrder(w, r)
		return
	}
	w.WriteHeader(http.StatusMethodNotAllowed)
}

func listOrders(w http.ResponseWriter, r *http.Request) {
	ordersMu.Lock()
	defer ordersMu.Unlock()
	arr := make([]Order, 0, len(orders))
	for _, o := range orders {
		arr = append(arr, o)
	}
	json.NewEncoder(w).Encode(arr)
}

func createOrder(w http.ResponseWriter, r *http.Request) {
	var req struct {
		UserID    int `json:"user_id"`
		ProductID int `json:"product_id"`
		Quantity  int `json:"quantity"`
	}
	body, _ := ioutil.ReadAll(r.Body)
	if err := json.Unmarshal(body, &req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "invalid json"})
		return
	}
	if req.UserID == 0 || req.ProductID == 0 || req.Quantity <= 0 {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "user_id, product_id and quantity required"})
		return
	}

	// Validate user and product by calling services (addresses via env)
	userSvc := getenv("USER_SERVICE_URL", "http://localhost:5002")
	prodSvc := getenv("PRODUCT_SERVICE_URL", "http://localhost:5001")

	if !remoteExists(fmt.Sprintf("%s/users/%d", userSvc, req.UserID)) {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "user not found"})
		return
	}
	if !remoteExists(fmt.Sprintf("%s/products/%d", prodSvc, req.ProductID)) {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(map[string]string{"error": "product not found"})
		return
	}

	ordersMu.Lock()
	id := nextID
	nextID++
	o := Order{ID: id, UserID: req.UserID, ProductID: req.ProductID, Quantity: req.Quantity, CreatedAt: time.Now()}
	orders[id] = o
	ordersMu.Unlock()

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(o)
}

func remoteExists(url string) bool {
	resp, err := http.Get(url)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	return resp.StatusCode >= 200 && resp.StatusCode < 300
}

func getenv(k, d string) string {
	v := os.Getenv(k)
	if v == "" {
		return d
	}
	// allow specifying with port only (e.g. 5001) - convenience for local runs
	if _, err := strconv.Atoi(v); err == nil {
		return "http://localhost:" + v
	}
	return v
}
