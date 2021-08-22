package database

import (
	"context"
	"fmt"
	"os"
	"reflect"

	"github.com/Sunkek/sunbot/settings/utils"
	"github.com/jackc/pgconn"
	"github.com/jackc/pgx/v4/pgxpool"
)

const defaultUser = "postgres"
const defaultPassword = "password"
const defaultHost = "postgres"
const defaultPort = "5432"
const defaultDatabase = "sb_db"

const CLEAN_START = `DO $$
BEGIN
    DROP TABLE IF EXISTS guilds;
END$$;`
const CREATE_GUILDS_TABLE = `CREATE TABLE IF NOT EXISTS guilds (
	id BIGINT, 
	PRIMARY KEY(id),

	welcome_channel_id BIGINT,
	welcome_initial_message_text VARCHAR,
	welcome_initial_message_embed VARCHAR,
	welcome_accept_message_text VARCHAR,
	welcome_accept_message_embed VARCHAR,
	leave_message_text VARCHAR,
	leave_message_embed VARCHAR
);`

var dbPool *pgxpool.Pool

func init() {
	dbpool, err := pgxpool.Connect(context.Background(), getDBURI())
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}

	cs := os.Getenv("CLEAN_START")
	if cs == "1" {
		dbpool.Exec(context.Background(), CLEAN_START)
	}

	dbpool.Exec(context.Background(), CREATE_GUILDS_TABLE)

	dbPool = dbpool
	//defer dbpool.Close()
}

func GetDB() *pgxpool.Pool {
	return dbPool
}

func getDBURI() string {
	host := os.Getenv("DB_HOST")
	if host == "" {
		host = defaultHost
	}
	port := os.Getenv("DB_PORT")
	if port == "" {
		port = defaultPort
	}
	user := os.Getenv("POSTGRES_USER")
	if user == "" {
		user = defaultUser
	}
	password := os.Getenv("POSTGRES_PASSWORD")
	if password == "" {
		password = defaultPassword
	}
	database := os.Getenv("POSTGRES_DB")
	if database == "" {
		database = defaultDatabase
	}

	return fmt.Sprintf("postgres://%v:%v@%v:%v/%v", user, password, host, port, database)
}

func BuildUpdateMap(input interface{}) (map[string]interface{}, error) {
	res := make(map[string]interface{})
	val := reflect.ValueOf(input)
	t := val.Type()
	for i := 0; i < val.NumField(); i++ {
		tag := t.Field(i).Tag.Get("json") // TODO add `db` tag?
		v := val.Field(i).Interface()
		if utils.KeyIsAllowed(tag) {
			if reflect.ValueOf(v).Kind() == reflect.Ptr && val.Field(i).IsNil() {
				continue
			}
			set, err := utils.AnythingToBool(v)
			if err != nil {
				return res, err
			}
			if !set {
				v = nil
			}
			res[tag] = v
		}
	}
	return res, nil
}

func unpackArgsAndExec(pool *pgxpool.Pool, query string, id int, args []interface{}) (pgconn.CommandTag, error) {
	switch len(args) {
	case 1:
		res, err := pool.Exec(context.Background(), query, id, args[0])
		return res, err
	case 2:
		res, err := pool.Exec(context.Background(), query, id, args[0], args[1])
		return res, err
	case 3:
		res, err := pool.Exec(context.Background(), query, id, args[0], args[1], args[2])
		return res, err
	default:
		res, err := pool.Exec(context.Background(), query, id)
		return res, err
	}
}
