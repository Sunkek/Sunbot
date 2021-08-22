package database

import (
	"context"
	"fmt"
)

const CREATE_GUILD_SETTINGS = `INSERT INTO guilds(id) VALUES ($1);`
const UPDATE_GUILD_SETTINGS = `UPDATE guilds SET %v WHERE id = $1;`

func buildUpdateGuildSettings(input map[string]interface{}) (string, []interface{}) {
	i := 2
	insert := ""
	args := make([]interface{}, len(input))
	for k, v := range input {
		if i != 2 {
			insert += ", "
		}
		insert += fmt.Sprintf("%v = $%v", k, i)
		args[i-2] = v
		i++
	}
	return fmt.Sprintf(UPDATE_GUILD_SETTINGS, insert), args
}

type NewGuildSettings struct {
	ID int `json:"id"`

	WelcomeChannelID           int     `json:"welcome_channel_id"`
	WelcomeInitialMessageText  *string `json:"welcome_initial_message_text"`
	WelcomeInitialMessageEmbed *string `json:"welcome_initial_message_embed"`
	WelcomeAcceptMessageText   *string `json:"welcome_accept_message_text"`
	WelcomeAcceptMessageEmbed  *string `json:"welcome_accept_message_embed"`
	LeaveMessageText           *string `json:"leave_message_text"`
	LeaveMessageEmbed          *string `json:"leave_message_embed"`
}

func (ns NewGuildSettings) Upsert() error {
	settings, err := BuildUpdateMap(ns)
	if err != nil {
		return err
	}
	query, args := buildUpdateGuildSettings(settings)
	pool := GetDB()

	res, err := unpackArgsAndExec(pool, query, ns.ID, args)
	if err != nil {
		return err
	}

	if res.RowsAffected() == 0 {
		_, err = pool.Exec(context.Background(), CREATE_GUILD_SETTINGS, ns.ID)
		if err != nil {
			return err
		}
		_, err = unpackArgsAndExec(pool, query, ns.ID, args)
		if err != nil {
			return err
		}
	}
	return err
}
