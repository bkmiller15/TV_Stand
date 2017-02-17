
 
APP=b
MCU=msp430g2553
MAP=msp430g2553_mem.map
 
AS=msp430-as
LD=msp430-ld
CP=msp430-gcc

ASFLAGS = -mmcu=$(MCU)
LDFLAGS = -T $(MAP)
 
all: $(APP).elf
 
$(APP).elf: 
	#$(CP) -mmcu=$(MCU) -Wall -Wextra -ggdb3 -Os -o $(APP).elf main.c
	$(CP) -mmcu=$(MCU) -Wall -Wextra -ggdb3 -o $(APP).elf main.c
	#$(LD) $(LDFLAGS) $(APP).o -o $(APP).elf
	msp430-objdump -D $(APP).elf > $(APP).lss
	msp430-size $(APP).elf
	msp430-objcopy -O ihex $(APP).elf $(APP).hex

#$(APP).o:
#	$(AS) $(ASFLAGS) $(APP).asm -o $(APP).o
 
install: all
	mspdebug rf2500 "prog $(APP).elf"
	#mspdebug --force-reset rf2500 "prog $(APP).elf"
 
#cycle_count: all
#naken430util -disasm $(APP).hex > $(APP)_cc.txt

debug: install
	mspdebug rf2500 gdb
 
gdb: 	
	msp430-gdb -ex="target remote localhost:2000" -ex="file $(APP).elf" 
#debug: all
#	clear
#	@echo -e "--------------------------------------------------------------------------------"
#	@echo -e "-- Make sure you are running mspdebug in another window --"
#	@echo -e "--------------------------------------------------------------------------------"
#	@echo -e "$$ # you can start it like this:"
#	@echo -e "$$ mspdebug rf2500 gdb\n"
#	msp430-gdb --command= $(APP).elf
 
clean:
	rm -f $(APP).o $(APP).elf $(APP).lss $(APP).hex 

