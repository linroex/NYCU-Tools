package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type transaction struct {
	Action    string
	Amount    int
	DeletedAt float64 `json:"deleted_at"`
}

type User struct {
	User         string
	Transactions []transaction
}

func main() {

	var user User
	var num int = 0

	dec := json.NewDecoder(os.Stdin)

	for {
		err := dec.Decode(&user)

		if err == io.EOF {
			break
		}

		if err != nil {
			fmt.Println("error")
		}
	}

	for _, trans := range user.Transactions {
		if trans.DeletedAt == 0 {
			num += trans.Amount
		}
	}

	fmt.Println(user.User, num)

}
