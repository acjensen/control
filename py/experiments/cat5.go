package main

import (
	"fmt"
)

type post struct {
	author    author
	title     string
	id        int
	published bool
}

type author struct {
	first_name string
	last_name  string
	biography  string
	photo_id   int
}

type techpost post

type publisher interface {
	publish()
}

func publish(p *post) {
	fmt.Printf("Publishing the post %s", p.title)
}

func main() {
	bp := new(post)
	bp.author.first_name = "AJ"
	fmt.Println(bp)
	bp.title = "the title hahahaha"
	publish(bp)
}
