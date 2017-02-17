/************************************************************************************************
 *
 *  Filename:	    main.c
 *
 *  Description:    This is the code 
 *
 *  Micro:          MSP430G2553
 *  Compiler:       MSP430GCC
 *
 *  Written by:     Brandon Miller
 *
 *  Version:        1.00
 *
 *  Last Modified on:   12/12/2014
 *************************************************************************************************/

//////////////////////////////////////////////////////
// INCLUDES                                         //
//////////////////////////////////////////////////////
#include <msp430.h>
#include <stdint.h>

// NODE ADDRESS
#define NODE 0x01

// CMD Enums
typedef enum 
{
	GS_ENUM = 0x00,
	DC_ENUM = 0x10,
}_CMD;


// Baud Rate Values : 115k2             
#define BAUDH_115k2 0x00             // 115k2 = 0x008B (139 decimal)
#define BAUDL_115k2 0x8B             // 16 MHz / 139 = 115,108 : 0.08% Error

// Timer Constants
#define GSCLK_TICS 0x1000           // 0x1000 = 4096 cycles


#define CMD_MASK 0xF0
#define NODE_MASK 0x0F


typedef enum
{
	FALSE = 0,
	TRUE = 1
} bool;



// Pin Definitions
#define PIN_VPRG BIT0
#define PIN_DCPRG BIT6


#define PIN_GSCLK BIT4  // P1.4
#define PIN_SCLK  BIT5  // P1.5
#define PIN_SIN   BIT7  // P1.7

#define PIN_XLAT  BIT1  // P2.1
#define PIN_BLANK BIT2  // P2.2

#define TA0_STOP   0x0030
#define TA0_UP     0x0010

#define INDEX_MAX 25


#define TXLED BIT6
#define RXLED BIT0
#define TXD BIT2
#define RXD BIT1

#define TXSPI BIT7





                             // Array for GS and DC Data.  Size is ((192 / 8) + 1) = 25
uint8_t S_Data[INDEX_MAX];   // Index starting at 1 and [0] is just extra space to flush
                             // out the TLC5940 

uint8_t S_Index = 1;         // Index variable for S_Data      

                             // Init_Complete is used to tell if the first DC and GS 
bool Init_Complete = FALSE;  // data has been loaded.  This then brings BLANK back LOW
                             // so that the LED's can start being displayed.

                             // If new data has been loaded to the TLC5490 this tells 
bool XLAT_Trig = FALSE;      // the code to trigger XLAT during the BLANK cycle.

_CMD Curr_CMD = DC_ENUM;     // Variable to save current cmd

// Function Prototypes
void stop_GSCycle();
void start_GSCycle();
__interrupt void TIMER0_A0_ISR(void); 
__interrupt void USCI_B0_TX_ISR(void); 
__interrupt void USCI0RX_ISR(void);
void get_uart();
uint8_t get_data_length(); 
  


//////////////////////////////////////////////////////
// MAIN                                             //
//////////////////////////////////////////////////////

int main(void)
{
  
	WDTCTL = WDTPW + WDTHOLD; // Stop WDT

    // Setup Clock For 16 MHz internal DCO 
    DCOCTL  = 0;
    BCSCTL1 = CALBC1_16MHZ;    
    DCOCTL  = CALDCO_16MHZ;  
    BCSCTL2 = 0x04;          // Divide SMCLK by 2
    //BCSCTL2 = 0x00;          // Divide SMCLK by 2
    BCSCTL3 = 0;

	// Setup PORT2
	P2SEL &= ~0xC0;
 	P2DIR |= 0xFF; // All P2.x outputs
   	P2OUT &= 0x00; // All P2.x reset
	P2OUT |= PIN_BLANK;    // Hold Blank HIGH until TLC5940 is initilized 
	P2OUT |= PIN_DCPRG;    // DC to register
	P2OUT |= PIN_VPRG;     // DC First


	// Setup PORT1
   	P1SEL |= RXD + TXD + PIN_GSCLK + TXSPI + PIN_SCLK; 
   	P1SEL2 |= RXD + TXD + TXSPI + PIN_SCLK; // P1.1 = RXD, P1.2=TXD
   	P1DIR |= RXLED + TXLED + PIN_GSCLK + PIN_SIN;
   	P1OUT &= 0x00;
	P2OUT |= PIN_BLANK;

	// Setup Timer
	TA0CCTL0 |= 0x0010;
	TA0CCR0 |= GSCLK_TICS;
	TA0CTL |= 0x0210;
	stop_GSCycle();


	// Setup Uart B SPI
   	UCB0CTL0 = 0x01; // Clear UC and hold in reset
   	UCB0CTL0 = 0x89;
   	UCB0CTL1 = 0x81; 
	IFG2 = 0x00;


	// Setup Uart A
   	//UCA0CTL0 = 0;                  // Clear UC control
   	//UCA0CTL0 |= UCMODE_1 + UCPEN;  // Enable Idle-Line Mode and Odd Parity
   	//UCA0CTL1 |= UCSSEL_2;          // Use SMCLK
	//UCA0MCTL = 0x02;               // UCBRSx = 1
   	//UCA0BR0 = 104;                 // 12MHz 115200 
   	//UCA0BR1 = 0x00;                // 12MHz 115200
   	//UCA0MCTL = UCBRS0; // Modulation UCBRSx = 5
	//UCA0CTL1 |= UCDORM;  		   // Set UCDORM so UART is dormant until addresss arives. 
   	//UCA0CTL1 &= ~UCSWRST; // **Initialize USCI state machine**


    	//UCA0BR1 = BAUDH_115k2;                       /* Baud = 115.2K Divisor is 0x03B = 139 decimal  */
    	//UCA0BR0 = BAUDL_115k2;                       /*    16 MHz / 139 = 115,108 : 0.08% Error       */

	UCA0BR1 = 0x00;                       /* Baud = 115.2K Divisor is 0x03B = 139 decimal  */
    	UCA0BR0 = 0x23; 

	UCA0MCTL = 0;                                /* No over-sampling selected                     */
	UCA0CTL0 |= UCMODE_1; //+ UCPEN;                // Enable Idle-Line Mode and Odd Parity
	UCA0STAT = 0;
	UCA0IRTCTL = 0;                              /* IrDA encoder/decoder off for Transmit         */
	UCA0CTL1 |= UCDORM;  		   // Set UCDORM so UART is dormant until addresss arives. 
	UCA0CTL1 &= ~UCSWRST; // **Initialize USCI state machine**
	IE2 = 0x00;


	    do
	    {
		/* flush any stale data */
		uint8_t dummy = UCA0RXBUF;
	    }
	    while (IFG2 & UCA0RXIFG);
	UCA0CTL1 |= UCSSEL_2;          // Use SMCLK


	
	// Start Timer and clock output
   	start_GSCycle();

   	__bis_SR_register(GIE); // 

	while (1) {  // Continuse loop
		get_uart();
	}       

}




void get_uart()
{
	uint8_t RX_BUFF;

	if (IFG2 & UCA0RXIFG) {    // IF there is a byte in the UART RXBUFFER, process the byte:

		//*****************************************************
		// Address Packet
		//*****************************************************
		if ((UCA0STAT & UCIDLE) == UCIDLE) {  // Address Packet

			UCA0CTL1 |= UCDORM;  		      // Set UCDORM so UART is dormant until addresss arives. 
			RX_BUFF = UCA0RXBUF;              // Get Buffer Data

			if ((RX_BUFF & NODE_MASK) == NODE   // IF Correct Node 
			//&&  (UCA0STAT & UCPE) == 0          // AND no parity error:
			){
	
				switch(RX_BUFF & CMD_MASK) {
					case GS_ENUM:
						P2OUT &= ~PIN_VPRG; 
						Curr_CMD = GS_ENUM;
						UCA0CTL1 &= ~UCDORM;  // Wake Uart
						Init_Complete = TRUE;
						break;

					case DC_ENUM:
						P2OUT |= PIN_VPRG; 
						Curr_CMD = DC_ENUM;
						UCA0CTL1 &= ~UCDORM;  // Wake Uart
						break;

					default:      // Not a valid command
						break;
				}
			}
		}


		//*****************************************************
		// Data Packet
		//*****************************************************
		else {                                // Data Packet
			//if ((UCA0STAT & UCPE) == 0) {     // IF no parity error:
				S_Data[S_Index] = UCA0RXBUF;  // Load buffer data into data array
			//}
			
			S_Index++;                        // Increment Index


			if (S_Index >= get_data_length()) {
				UCA0CTL1 |= UCDORM;  		  // Set UCDORM so UART is dormant until addresss arives. 
				S_Index = 0;                  // Set index so it can be used by B0TX uart
				UCB0TXBUF = S_Data[S_Index];  // Load serial transmit buffer with first value
				S_Index++;                    // Increment Index

				UCB0CTL1 &= ~0x01;          // Enable uart
				IE2 |= 0x08;                // Reenable interupt
			}
		}
	}
}
    






uint8_t get_data_length() {

	uint8_t length = 0;

	if (Curr_CMD == GS_ENUM) {
		length = 25;
	} 
	else if (Curr_CMD == DC_ENUM) {
		length = 13;
	}

	return length;
}



	
#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI_B0_TX_ISR(void) 
{

	UCB0TXBUF = S_Data[S_Index];  // Load serial transmit buffer with first value

	S_Index++;                    // Increment Index


	if (S_Index >= get_data_length()) {
		S_Index = 1;                  // Set index so it can be used by B0TX uart
		XLAT_Trig = TRUE;   

		UCB0CTL1 |= 0x01;          // Disable uart
		IE2 &= ~0x08;              // Clear interupt
	}
}








/************************************************************************************************
 * Title:     	    void TIMER0_A0_ISR()
 *
 * Description:     	
 *
 * Inputs:     		none
 * Outputs:    		none
 * Variables:
 *
 * Author:          Brandon Miller
 * Last Revised On: 12/18/2014
 **************************************************************************************************/
#pragma vector=TIMER0_A0_VECTOR
__interrupt void TIMER0_A0_ISR() 
{
 	stop_GSCycle();             // Stop the GSCycle 	

	P2OUT |= PIN_BLANK;         // Bring BLANK HIGH

	if (XLAT_Trig) { //IF Xlat needs to be set

		P2OUT |= PIN_XLAT;
		P2OUT &= ~PIN_XLAT;

		XLAT_Trig = FALSE;   
	}

	if (Init_Complete == TRUE) {   // Once 
		P2OUT &= ~PIN_BLANK;
	
		
	}
	start_GSCycle();

}




/************************************************************************************************
 * Title:     		stop_GSCycle()
 *
 * Description:     Stops the GS Cycle by disabling the GSCLK signal and also stoping and 
 *                  clearing Timer A that is counting the GS Clock pulses  	
 *
 * Inputs:     		none
 * Outputs:    		none
 * Variables:
 *
 * Author:          Brandon Miller
 * Last Revised On: 12/18/2014
 **************************************************************************************************/
void stop_GSCycle() 
{
	P1SEL &= ~PIN_GSCLK;    // Disable clock output

	TA0CTL &= ~TA0_STOP;    // Stop the timer
	TAR = 0;                // Clear out the timer
}

/************************************************************************************************
 * Title:     		start_GSCycle()
 *
 * Description:     Starts the GS Cycle by enabling the GSCLK signal and also starting and 
 *                  clearing Timer A that is counting the GS Clock pulses  	
 *
 * Inputs:     		none
 * Outputs:    		none
 * Variables:
 *
 * Author:          Brandon Miller
 * Last Revised On: 12/18/2014
 **************************************************************************************************/
void start_GSCycle() 
{
	TAR = 0;                // Clear out the timer
	TA0CTL |= TA0_UP;    	// Start the timer
	

   	P1SEL |= PIN_GSCLK;     // Enable clock output
}


