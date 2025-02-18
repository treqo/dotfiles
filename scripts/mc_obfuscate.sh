#!/bin/bash

FONT="MinecraftEnchantment"

obfuscate() {
    local text="$1"
    local length=${#text}
    local chars=("ᒷ" "ꖎ" "ᔑ" "𝙹" "ᓵ" "⎓" "╎" "⋮" "ꖌ" "リ" "ᒲ" "𝙹" "ᑑ" "⚍" "ᒲ" "𝙹")
    local obf_text=""

    for (( i=0; i<length; i++ )); do
        obf_text+="${chars[RANDOM % ${#chars[@]}]}"
    done

    echo "$obf_text"
}

"$@" | while IFS= read -r line; do
    obf_line=$(obfuscate "$line")
    echo -e "\033[38;5;208m$obf_line\033[0m"  # Display in obfuscated format (orange)
    sleep 0.2                                 # Delay for effect
    echo "$line"                              # Reveal actual text
    sleep 0.2
done



