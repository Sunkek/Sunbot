package handlers

import (
	"github.com/labstack/echo/v4"
)

func DiscordUserSet(c echo.Context) error {
	// Read new setting
	// Save to DB
	// Save to Redis
	return c.String(500, "Not implemented")
}
