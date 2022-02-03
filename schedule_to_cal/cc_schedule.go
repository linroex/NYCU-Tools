package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
	"regexp"
	"strings"
	"text/template"
	"time"
)

type CalendarEvent struct {
	StartDt string
	EndDt   string
}

var dateRegex = regexp.MustCompile(`(\d\d)/(\d\d) \(.\)`)
var timeRegex = regexp.MustCompile(`(\d\d:\d\d)-(\d\d:\d\d)`)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	schedules := []CalendarEvent{}
	previousLine := ""
	calDate := ""
	scheduleEvent := CalendarEvent{}

	for scanner.Scan() {
		currentLine := strings.Trim(scanner.Text(), " ")

		currentLineMatch := timeRegex.FindStringSubmatch(currentLine)
		previousLineMatch := timeRegex.FindStringSubmatch(previousLine)

		if dateRegex.MatchString(currentLine) {
			if scheduleEvent.EndDt != "" {
				schedules = append(schedules, scheduleEvent)
			}
			calDate = getCalDate(currentLine)
			scheduleEvent = CalendarEvent{
				StartDt: calDate + getCalTime(currentLineMatch[1]),
				EndDt:   calDate + getCalTime(currentLineMatch[2]),
			}
		} else if timeRegex.MatchString(currentLine) {
			if currentLineMatch[1] != previousLineMatch[2] {
				schedules = append(schedules, scheduleEvent)
				scheduleEvent = CalendarEvent{
					StartDt: calDate + getCalTime(currentLineMatch[1]),
					EndDt:   calDate + getCalTime(currentLineMatch[2]),
				}
			}
			scheduleEvent.EndDt = calDate + getCalTime(currentLineMatch[2])
		}

		previousLine = currentLine

	}

	schedules = append(schedules, scheduleEvent)

	fmt.Println(generateICSOutput(schedules))
}

func getCalDate(line string) string {
	currentDate := time.Now()

	if dateRegex.MatchString(line) {
		match := dateRegex.FindStringSubmatch(line)

		calYear := currentDate.Year()
		if match[1] == "01" && currentDate.Month() == 12 {
			calYear += 1
		}

		return fmt.Sprintf("%d%s%sT", calYear, match[1], match[2])
	}

	return ""
}

func getCalTime(timeStr string) string {
	return strings.ReplaceAll(timeStr, ":", "") + "00"
}

func generateICSOutput(events []CalendarEvent) string {
	icsTemplateString :=
		`BEGIN:VCALENDAR
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:-//Test Cal//EN
VERSION:2.0
{{ range $index, $event := . }}BEGIN:VEVENT
UID:{{$index}}
DTSTART;VALUE=DATE:{{$event.StartDt}}
DTEND;VALUE=DATE:{{$event.EndDt}}
SUMMARY:值班
END:VEVENT
{{ end }}END:VCALENDAR`
	icsTemplate, _ := template.New("ics").
		Parse(icsTemplateString)

	var result bytes.Buffer
	icsTemplate.Execute(&result, events)
	return result.String()
}
