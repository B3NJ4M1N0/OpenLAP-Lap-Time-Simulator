classdef OpenGUI
    %OPENGUI Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        window
        GUI
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
            app.GUI.title.FontSize = 35;
            app.GUI.title.Units = 'normalized';
            app.GUI.title.Position = [0.05 0.8 0.4 0.1];

            % Set up the user inputs
            app.GUI.simulationList = uicontrol('parent',app.GUI.window,'Style','listbox');
            app.GUI.simulationList.String = {'OpenVEHICLE','OpenTrack','OpenDRAG','OpenLap'};
            app.GUI.simulationList.Units = 'normalized';
            app.GUI.simulationList.Position = [0.05 0.05 0.4 0.7];
            app.GUI.Callback = @app.simulationListChanged;

            % Create a 'run' button
            app.GUI.runButton = uicontrol('parent',app.GUI.window,'Style','pushbutton');
            app.GUI.runButton.String = 'Run Simulation';
            app.GUI.runButton.Units = 'normalized';
            app.GUI.runButton.Position = [0.85 0.1 0.1 0.1];
            app.GUI.runButton.Callback = @app.runButtonPressed;

        end

        function simulationListChanged(app, ~, ~)
            % Changes the GUI depending on which simulation is chosen from
            % the selection list
        end

        function runButtonPressed(app, ~, ~)
            % Runs the functions based on the user inputs
        end

        function runOpenDRAG(app, ~, ~)
            % Runs the OpenDRAG function with the given GUI inputs
        end

        function runOpenLAP(app, ~, ~)
            % Runs the OpenLAP function with the given GUI inputs
        end

        function runOpenTRACK(app, ~, ~)
            % Runs the OpenTRACK function with the given GUI inputs
        end

        function runOpenVEHICLE(app, ~, ~)
            % Runs the OpenVEHICLE function with the given GUI inputs
        end

        function app = OpenGUI()
            %OPENGUI Construct an instance of this class
            %   Detailed explanation goes here
            app.createComponents();
        end
    end
end

