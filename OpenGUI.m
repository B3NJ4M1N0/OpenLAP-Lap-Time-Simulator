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
            app.GUI.window.Position = [0.1 0.1 0.8 0.8];

            % Set up the title text
            app.GUI.title = uicontrol('parent',app.GUI.window,'Style','text');
            app.GUI.title.String = 'OpenGUI';
            app.GUI.title.FontSize = 20;
            app.GUI.title.Units = 'normalized';
            app.GUI.title.Position = [0.025 0.85 0.1 0.1];

            % Set up the user inputs
            app.GUI.simulationList = uicontrol('parent',app.GUI.window,'Style','listbox');
            app.GUI.simulationList.String = {'OpenVEHICLE','OpenTRACK','OpenDRAG','OpenLap'};
            app.GUI.simulationList.Units = 'normalized';
            app.GUI.simulationList.Position = [0.025 0.7 0.1 0.15];
            app.GUI.simulationList.Callback = @app.simulationListChanged;

            % First reset the simulation panel
            % TODO: There is no garbage collection on this, turn into function app.resetSimPanel().
            % TODO: This panel should just be a list that updates with everything in it.
            app.GUI.simulationPanel = uipanel('parent', app.GUI.window);
            app.GUI.simulationPanel.Units = 'normalized';
            app.GUI.simulationPanel.Position = [0.025 0.05 0.2 0.5];
            app.GUI.simulationPanel.Title = 'Simulation Setup';

            % TODO: add in a results pane on the right that will hold the plots.
            app.GUI.resultsPane = uipanel('parent', app.GUI.window);
            app.GUI.resultsPane.Units = 'normalized';
            app.GUI.resultsPane.Position = [0.3 0.1 0.6 0.8];
            app.GUI.resultsPane.Title = 'Results';

            % Create a 'run' button
            app.GUI.runButton = uicontrol('parent',app.GUI.window,'Style','pushbutton');
            app.GUI.runButton.String = 'Run Simulation';
            app.GUI.runButton.Units = 'normalized';
            app.GUI.runButton.Position = [0.85 0.1 0.1 0.1];
            app.GUI.runButton.Callback = @app.runButtonPressed;

        end

        function app = simulationListChanged(app, ~, ~)
            % Changes the GUI depending on which simulation is chosen from
            % the selection list

            % Sets up the available buttons for each simulation type

            % First reset the simulation panel
            app.GUI.simulationPanel = uipanel('parent', app.GUI.window);
            app.GUI.simulationPanel.Units = 'normalized';
            app.GUI.simulationPanel.Position = [0.025 0.05 0.2 0.5];
            app.GUI.simulationPanel.Title = 'Simulation Setup';

            listIndex = app.GUI.simulationList.Value;
            simulationName = app.GUI.simulationList.String{listIndex};
            
            if strcmp(simulationName,'OpenVEHICLE')
            % Car file selection for OpenVEHICLE
                app.GUI.vehicleSelectionBox = uicontrol('parent', app.GUI.simulationPanel, 'Style','popupmenu');
                app.GUI.vehicleSelectionBox.Units = 'normalized';
                app.GUI.vehicleSelectionBox.Position = [0.1 0.8 0.7 0.1];
                vehicleFiles = dir('Vehicles');
                vehicleFiles = vehicleFiles(~(strcmp({vehicleFiles.name}, '.') | strcmp({vehicleFiles.name}, '..')), :);
                app.GUI.vehicleSelectionBox.String = {vehicleFiles.name};

            elseif strcmp(simulationName,'OpenTRACK')
            % Track file selection for OpenTRACK
                app.GUI.trackSelectionBox = uicontrol('parent', app.GUI.simulationPanel, 'Style','popupmenu');
                app.GUI.trackSelectionBox.Units = 'normalized';
                app.GUI.trackSelectionBox.Position = [0.1 0.8 0.7 0.1];
                trackFiles = dir('Tracks');
                trackFiles = trackFiles(~(strcmp({trackFiles.name}, '.') | strcmp({trackFiles.name}, '..')), :);
                app.GUI.trackSelectionBox.String = {trackFiles.name};
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
                resultsPlot = app.runOpenVEHICLE;
                % Update the app.GUI.resultsPanel here with 'resultsPlot'.
            elseif strcmp(simulationName,'OpenTRACK')
                resultsPlot = app.runOpenTRACK;
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
            filename = fullfile( 'Tracks', app.GUI.trackSelectionBox.String{app.GUI.trackSelectionBox.Value} );
            app.TRACK = OpenTRACK(filename);
            app.TRACK.mode = 'shape data';
            app.TRACK.log_mode = 'speed & latacc';
            % Get the plot object from OpenTRACK and assign it to the results panel.
            trackPlot = app.TRACK.plotPane; % this doesn't exist yet
            trackPlot.Parent = app.GUI.resultsPane;
            % Attempt some garbage collection
            close(app.TRACK.fig);
        end

        function app = runOpenVEHICLE(app, ~, ~)
            % Runs the OpenVEHICLE function with the given GUI inputs
            filename = app.GUI.vehicleSelectionBox.String{app.GUI.vehicleSelectionBox.Value};
            app.VEHICLE = OpenVEHICLE(filename);

        end

        function app = OpenGUI()
            %OPENGUI Construct an instance of this class
            %   Detailed explanation goes here
            app.createComponents();
        end
    end
end

