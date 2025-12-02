`timescale 1ns / 1ps

module tb_industrial_pump_monitor();
    reg  S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb;
    wire A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb;

    industrial_pump_monitor DUT (
        .S1(S1_tb), .S2(S2_tb), .S3(S3_tb), .S4(S4_tb), .S5(S5_tb), .S6(S6_tb),
        .A1(A1_tb), .A2(A2_tb), .A3(A3_tb), .A4(A4_tb), .A5(A5_tb), .A6(A6_tb)
    );

    initial begin
        $dumpfile("simulation_waveform.vcd");
        $dumpvars(0, tb_industrial_pump_monitor);

        $display("Time | S1 S2 S3 S4 S5 S6 | A1 A2 A3 A4 A5 A6 | Test Case Description");

        #10 S1_tb=1'b1; S2_tb=1'b1; S3_tb=1'b1; S4_tb=1'b1; S5_tb=1'b0; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | NORMAL_OPERATION", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b1; S2_tb=1'b0; S3_tb=1'b1; S4_tb=1'b1; S5_tb=1'b0; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | FAULT_LOW_PRESSURE", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b1; S2_tb=1'b1; S3_tb=1'b0; S4_tb=1'b1; S5_tb=1'b0; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | FAULT_LOW_WATER_LEVEL", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b1; S2_tb=1'b1; S3_tb=1'b1; S4_tb=1'b0; S5_tb=1'b0; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | FAULT_NO_FLOW_DRY_RUN", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b1; S2_tb=1'b1; S3_tb=1'b1; S4_tb=1'b1; S5_tb=1'b1; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | FAULT_MOTOR_OVERHEAT", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b1; S2_tb=1'b1; S3_tb=1'b1; S4_tb=1'b1; S5_tb=1'b0; S6_tb=1'b1;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | FAULT_ABNORMAL_VIBRATION", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #10 S1_tb=1'b0; S2_tb=1'b1; S3_tb=1'b1; S4_tb=1'b1; S5_tb=1'b0; S6_tb=1'b0;
        #1  $display("%4t | %b  %b  %b  %b  %b  %b  | %b  %b  %b  %b  %b  %b  | SYSTEM_POWER_OFF_SHUTDOWN", 
                     $time, S1_tb, S2_tb, S3_tb, S4_tb, S5_tb, S6_tb, 
                     A1_tb, A2_tb, A3_tb, A4_tb, A5_tb, A6_tb);

        #20 $finish;
    end

endmodule
