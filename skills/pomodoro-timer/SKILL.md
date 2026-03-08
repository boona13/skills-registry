---
name: pomodoro-timer
description: "Pomodoro technique timer — set focused work sessions with break reminders"
triggers:
  - "pomodoro"
  - "focus timer"
  - "work session"
  - "take a break"
  - "25 minutes"
tools:
  - "shell_exec"
  - "notify"
priority: 5
---

# Pomodoro Timer

Help the user manage focused work sessions using the Pomodoro Technique.

## How It Works

- A pomodoro is a 25-minute focused work session
- After each pomodoro, take a 5-minute break
- After 4 pomodoros, take a 15-30 minute long break

## Steps

1. When the user asks to start a pomodoro, use `shell_exec` to run a background timer:
   ```
   (sleep 1500 && echo "Pomodoro complete") &
   ```
2. Use `notify` to send a notification when the timer starts
3. Remind the user what they're focusing on
4. When the timer ends, use `notify` to alert them to take a break

## Commands

- "start a pomodoro" — Begin a 25-minute session
- "take a break" — Start a 5-minute break timer
- "pomodoro status" — Check remaining time
- "how many pomodoros today" — Check session count

## Output Format

When starting a session:
- Confirm the focus topic
- Show the end time
- Encourage the user to stay focused
