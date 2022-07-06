classdef OpenGUI < handle
    %OPENGUI Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        window
        GUI
        VEHICLE
        TRACK
        DRAG
        LAP
    end
    
    methods

        function createComponents(app)
            % Initialise the app and create the GUI
            app.GUI.window = figure;
            app.GUI.window.Units = 'normalized';
            app.GUI.window.Position = [0.1 0.1 0.4 0.4];

            % Set up the title text
            app.GUI.title = uicontrol('parent',app.GUI.window,'Style','text');
            app.GUI.title.String = 'OpenGUI';
            app.GUI.title.FontSize = 20;
            app.GUI.title.Units = 'normalized';
            app.GUI.title.Position = [0.025 0.85 0.1 0.1];

            % Set up the user inputs
            app.GUI.simulationList = uicontrol('parent',app.GUI.window,'Style','listbox');
            app.GUI.simulationList.String = {'OpenVEHICLE','OpenTrack','OpenDRAG','OpenLap'};
            app.GUI.simulationList.Units = 'normalized';
            app.GUI.simulationList.Position = [0.025 0.7 0.1 0.15];
            app.GUI.simulationList.Callback = @app.simulationListChanged;

            % Create a 'run' button
            app.GUI.runButton = uicontrol('parent',app.GUI.window,'Style','pushbutton');
            app.GUI.runButton.String = 'Run Simulation';
            app.GUI.runButton.Units = 'normalized';
            app.GUI.runButton.Position = [0.85 0.1 0.1 0.1];
            app.GUI.runButton.Callback = @app.runButtonPressed;

            % First reset the right hand side of the GUI
            app.GUI.simulationPanel = uipanel('parent', app.GUI.window);
            app.GUI.simulationPanel.Units = 'normalized';
            app.GUI.simulationPanel.Position = [0.55 0.25 0.4 0.7];
            app.GUI.simulationPanel.Title = 'Simulation Setup';

        end

        function app = simulationListChanged(app, ~, ~)
            % Changes the GUI depending on which simulation is chosen from
            % the selection list

            % Sets up the available buttons for each simulation type

            % First reset the right hand side of the GUI
            app.GUI.simulationPanel = uipanel('parent', app.GUI.window);
            app.GUI.simulationPanel.Units = 'normalized';
             app.GUI.simulationPanel.Position = [0.55 0.25 0.4 0.7];
            app.GUI.simulationPanel.Title = 'Simulation Setup';

            listIndex = app.GUI.simulationList.Value;
            simulationName = app.GUI.simulationList.String{listIndex};
            
            if strcmp(simulationName,'OpenVEHICLE')
            % Car file selection for OpenVEHICLE
                app.GUI.vehicleSelectionBox = uicontrol('parent', app.GUI.simulationPanel, 'Style','popupmenu');
                app.GUI.vehicleSelectionBox.Units = 'normalized';
                app.GUI.vehicleSelectionBox.Position = [0.1 0.8 0.3 0.1];
                vehicleFiles = dir('Vehicles');
                vehicleFiles = vehicleFiles(~(strcmp({vehicleFiles.name}, '.') | strcmp({vehicleFiles.name}, '..')), :);
                app.GUI.vehicleSelectionBox.String = {vehicleFiles.name};

            elseif strcmp(simulationName,'OpenTRACK')
            % Track file selection for OpenTRACK
            elseif strcmp(simulationName,'OpenLAP')
            % Lap file selection for OpenLAP
            elseif strcmp(simulationName,'OpenDRAG')
            % Set up GUI for OpenDRAG
            end

        end

        function runButtonPressed(app, ~, ~)

            listIndex = app.GUI.simulationList.Value;
            simulationName = app.GUI.simulationList.String{listIndex};

            % Runs the functions based on the user inputs
            if strcmp(simulationName,'OpenVEHICLE')
                app.runOpenVEHICLE;
            elseif strcmp(simulationName,'OpenTRACK')
                app.runOpenTRACK;
            elseif strcmp(simulationName,'OpenLAP')
                app.runOpenLAP;
            elseif strcmp(simulationName,'OpenDRAG')
                app.runOpenDRAG;
            end
        end

        function app = runOpenDRAG(app, ~, ~)
            % Runs the OpenDRAG function with the given GUI inputs
        end

        function app = runOpenLAP(app, ~, ~)
            % Runs the OpenLAP function with the given GUI inputs
        end

        function app = runOpenTRACK(app, ~, ~)
            % Runs the OpenTRACK function with the given GUI inputs
        end

        function app = runOpenVEHICLE(app, ~, ~)
            % Runs the OpenVEHICLE function with the given GUI inputs
            app.VEHICLE = OpenVEHICLE;
            app.VEHICLE.filename = app.GUI.vehicleSelectionBox.String{app.GUI.vehicleSelectionBox.Value};

        end

        function app = OpenGUI()
            %OPENGUI Construct an instance of this class
            %   Detailed explanation goes here
            app.createComponents();
        end
    end
end

