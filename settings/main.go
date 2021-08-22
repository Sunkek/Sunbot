package main

import (
	"github.com/Sunkek/sunbot/settings/handlers"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Routes
	d := e.Group("/discord")
	g := d.Group("/guild")
	u := d.Group("/user")
	g.POST("/set/:id", handlers.DiscordGuildSet)
	u.POST("/set/:id", handlers.DiscordUserSet)

	// Start server
	port := "8001" //os.Getenv("SETTINGS_PORT")
	e.Logger.Fatal(e.Start(":" + port))
}
