package handlers

import (
	"net/http"
	"strconv"

	"github.com/Sunkek/sunbot/settings/database"
	"github.com/labstack/echo/v4"
)

func DiscordGuildSet(c echo.Context) error {
	// Read new setting
	id := c.Param("id")
	gID, err := strconv.Atoi(id)
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	db := new(echo.DefaultBinder)
	ns := new(database.NewGuildSettings)
	if err := db.BindBody(c, &ns); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	ns.ID = gID
	// Save to DB
	err = ns.Upsert()
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	// Save to Redis

	return c.String(200, "OK")
}
