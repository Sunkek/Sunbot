package utils

var allowedKeys = []string{
	"welcome_channel_id",
	"welcome_initial_message_text",
	"welcome_initial_message_embed",
	"welcome_accept_message_text",
	"welcome_accept_message_embed",
	"leave_message_text",
	"leave_message_embed",
}

func StringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func KeyIsAllowed(k string) bool {
	return StringInSlice(k, allowedKeys)
}
