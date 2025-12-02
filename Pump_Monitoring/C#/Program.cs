using System;
using System.Threading;

public class PumpMonitoringSystem
{
    // --- Sensor States (Inputs) ---
    public bool S1_Current { get; private set; }
    public bool S2_Pressure { get; private set; }
    public bool S3_Level { get; private set; }
    public bool S4_Flow { get; private set; }
    public bool S5_Temperature { get; private set; }
    public bool S6_Vibration { get; private set; }

    // --- Actuator States (Outputs) ---
    public bool A1_Relay { get; private set; }
    public bool A2_Motor { get; private set; }
    public bool A3_Valve { get; private set; }
    public bool A4_IndicatorLed { get; private set; }
    public bool A5_AlarmBuzzer { get; private set; }
    public bool A6_DigitalDisplay { get; private set; }

    public void SetSensorStates(bool s1, bool s2, bool s3, bool s4, bool s5, bool s6)
    {
        S1_Current = s1;
        S2_Pressure = s2;
        S3_Level = s3;
        S4_Flow = s4;
        S5_Temperature = s5;
        S6_Vibration = s6;
    }

    public void ComputeLogic()
    {
        A1_Relay = S1_Current && S2_Pressure && S3_Level && S4_Flow && !S5_Temperature && !S6_Vibration;
        A2_Motor = A1_Relay;
        A3_Valve = A1_Relay;
        A5_AlarmBuzzer = !S2_Pressure || !S3_Level || !S4_Flow || S5_Temperature || S6_Vibration;
        A4_IndicatorLed = A1_Relay || A5_AlarmBuzzer;
        A6_DigitalDisplay = true;
    }

    public void PrintStatus(string scenarioDescription)
    {
        Console.WriteLine($"\n--- SCENARIO: {scenarioDescription} ---");
        Console.WriteLine("[INPUTS]  S1:{0} S2:{1} S3:{2} S4:{3} S5:{4} S6:{5}",
                          S1_Current ? 1 : 0, 
                          S2_Pressure ? 1 : 0, 
                          S3_Level ? 1 : 0, 
                          S4_Flow ? 1 : 0, 
                          S5_Temperature ? 1 : 0, 
                          S6_Vibration ? 1 : 0);
        
        Console.WriteLine("[OUTPUTS] A1:{0} A2:{1} A3:{2} A4:{3} A5:{4} A6:{5}",
                          A1_Relay ? 1 : 0, 
                          A2_Motor ? 1 : 0, 
                          A3_Valve ? 1 : 0, 
                          A4_IndicatorLed ? 1 : 0, 
                          A5_AlarmBuzzer ? 1 : 0, 
                          A6_DigitalDisplay ? 1 : 0);
        
        string systemState = A1_Relay ? "NORMAL OPERATION" : (A5_AlarmBuzzer ? "FAULT DETECTED" : "STANDBY/OFF");
        Console.WriteLine($"System State: {systemState}");
    }
}

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("======================================================");
        Console.WriteLine("  C# Simulation for Industrial Pump Monitoring System  ");
        Console.WriteLine("======================================================\n");

        var system = new PumpMonitoringSystem();
        
        // Scenario 1: Normal Operation
        system.SetSensorStates(true, true, true, true, false, false);
        system.ComputeLogic();
        system.PrintStatus("Normal Operation");
        Thread.Sleep(1000);

        // Scenario 2: Low/Over Pressure
        system.SetSensorStates(true, false, true, true, false, false);
        system.ComputeLogic();
        system.PrintStatus("Low/Over Pressure");
        Thread.Sleep(1000);

        // Scenario 3: Low Water Level
        system.SetSensorStates(true, true, false, true, false, false);
        system.ComputeLogic();
        system.PrintStatus("Low Water Lavel");
        Thread.Sleep(1000);

        // Scenario 4: No Flow
        system.SetSensorStates(true, true, true, false, false, false);
        system.ComputeLogic();
        system.PrintStatus("No Flow (Dry Run)");
        Thread.Sleep(1000);

        // Scenario 5: Overheat
        system.SetSensorStates(true, true, true, true, true, false);
        system.ComputeLogic();
        system.PrintStatus("Motor Overheat");
        Thread.Sleep(1000);

        // Scenario 6: Abnormal Vibration
        system.SetSensorStates(true, true, true, true, false, true);
        system.ComputeLogic();
        system.PrintStatus("Abnormal Vibration");
        Thread.Sleep(1000);

        // Scenario 7: Inactive Current
        system.SetSensorStates(false, true, true, true, false, false);
        system.ComputeLogic();
        system.PrintStatus("Inactive Current (System Shut Down)");
        Thread.Sleep(1000);

        Console.WriteLine("\n======================================================");
        Console.WriteLine("Simulation finished successfully.");
        Console.WriteLine("Press any key to exit.");
        Console.ReadKey();
    }
}
