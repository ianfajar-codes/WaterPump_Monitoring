module industrial_pump_monitor (
    input wire S1, S2, S3, S4, S5, S6,
    output wire A1, A2, A3, A4, A5, A6
);
    assign A1 = S1 & S2 & S3 & S4 & ~S5 & ~S6;
    assign A2 = A1;
    assign A3 = A1;
    assign A5 = ~S2 | ~S3 | ~S4 | S5 | S6;
    assign A4 = A1 | A5;
    assign A6 = 1'b1;
endmodule
