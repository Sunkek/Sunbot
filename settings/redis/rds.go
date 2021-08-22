package rds

import (
	"os"

	"github.com/go-redis/redis/v8"
)

var rdsClient *redis.Client

func init() {
	host := os.Getenv("REDIS_HOST")
	port := os.Getenv("REDIS_PORT")
	rdb := redis.NewClient(&redis.Options{
		Addr:     host + ":" + port,
		Password: "", // No password set
		DB:       0,  // Use default DB
	})
	rdsClient = rdb
}

func GetRds() *redis.Client {
	return rdsClient
}
