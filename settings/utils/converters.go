package utils

import "fmt"

func numToBool(input interface{}) bool {
	return input != 0
}

func AnythingToBool(input interface{}) (bool, error) {
	switch input.(type) {
	case int:
		return numToBool(input), nil
	case uint:
		return numToBool(input), nil
	case uint8:
		return numToBool(input), nil
	case uint16:
		return numToBool(input), nil
	case uint32:
		return numToBool(input), nil
	case uint64:
		return numToBool(input), nil
	case int8:
		return numToBool(input), nil
	case int16:
		return numToBool(input), nil
	case int32:
		return numToBool(input), nil
	case int64:
		return numToBool(input), nil
	case float32:
		return numToBool(input), nil
	case float64:
		return numToBool(input), nil
	case string:
		return input != "", nil

	default:
		return false, fmt.Errorf("unknown type, can't convert to boolean")
	}
}
