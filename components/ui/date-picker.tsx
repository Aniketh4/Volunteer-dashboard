"use client"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

interface DatePickerProps {
  value?: Date | null
  onChange: (date: Date | null) => void
  placeholder?: string
  id?: string
}

export function DatePicker({ value, onChange, placeholder = "Pick a date", id }: DatePickerProps) {
  const handleSelect = (date: Date | undefined) => {
    onChange(date || null)
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          id={id}
          variant={"outline"}
          className={cn("w-full justify-start text-left font-normal", !value && "text-muted-foreground")}
        >
          <CalendarIcon className="mr-2 h-4 w-4" />
          {value ? format(value, "PPP") : <span>{placeholder}</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar 
          mode="single" 
          selected={value || undefined} 
          onSelect={handleSelect}
          initialFocus 
        />
      </PopoverContent>
    </Popover>
  )
}

