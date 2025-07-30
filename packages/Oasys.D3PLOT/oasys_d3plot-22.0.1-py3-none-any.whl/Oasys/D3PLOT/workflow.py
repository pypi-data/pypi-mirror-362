import Oasys.gRPC


# Metaclass for static properties and constants
class WorkflowType(type):
    _consts = {'UNIT_SYSTEM_NONE', 'UNIT_SYSTEM_U1', 'UNIT_SYSTEM_U2', 'UNIT_SYSTEM_U3', 'UNIT_SYSTEM_U4', 'UNIT_SYSTEM_U5', 'UNIT_SYSTEM_U6'}

    def __getattr__(cls, name):
        if name in WorkflowType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError("Workflow class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the constants we define then error
        if name in WorkflowType._consts:
            raise AttributeError("Cannot set Workflow class constant '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Workflow(Oasys.gRPC.OasysItem, metaclass=WorkflowType):


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        if self._handle is None:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Workflow instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def ModelIdFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the id of a model selected by the user by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the unit system for.
            If the workflow is run from the workflow menu and the name argument is not defined, it is the index in the list of
            models selected by the user.
            If the workflow is run from the workflow menu and the name argument is defined, it is the index of the model that
            has user data for the named workflow, out of the list of models selected by the user.
            If the workflow is run from REPORTER, it is the index in the list of all the models loaded in the session that 
            have user data for the named workflow
        workflow_name : string
            Optional. The workflow name to return the model id for

        Returns
        -------
        int
            integer
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelIdFromIndex", model_index, workflow_name)

    def ModelUnitSystemFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the unit system of a model selected by the user by index (starting at 0).
        Will be Workflow.UNIT_SYSTEM_NONE or
        Workflow.UNIT_SYSTEM_U1 or
        Workflow.UNIT_SYSTEM_U2 or
        Workflow.UNIT_SYSTEM_U3 or
        Workflow.UNIT_SYSTEM_U4 or
        Workflow.UNIT_SYSTEM_U5 or
        Workflow.UNIT_SYSTEM_U6

        Parameters
        ----------
        model_index : integer
            The index of the model to return the unit system for.
            If the workflow is run from the workflow menu and the name argument is not defined, it is the index in the list of
            models selected by the user.
            If the workflow is run from the workflow menu and the name argument is defined, it is the index of the model that
            has user data for the named workflow, out of the list of models selected by the user.
            If the workflow is run from REPORTER, it is the index in the list of all the models loaded in the session that 
            have user data for the named workflow
        workflow_name : string
            Optional. The workflow name to return the unit system for

        Returns
        -------
        int
            integer
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelUnitSystemFromIndex", model_index, workflow_name)

    def ModelUserDataBuildFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the build number of the program that was used to write out the
        user data of a model for the selected workflow by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the program build number for
        workflow_name : string
            Optional. The workflow name to return the build number for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the build number for the first user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelUserDataBuildFromIndex", model_index, workflow_name)

    def ModelUserDataFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the user data associated with a model by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the user data for.
            If the workflow is run from the workflow menu and the name argument is not defined, it is the index in the list of
            models selected by the user.
            If the workflow is run from the workflow menu and the name argument is defined, it is the index of the model that
            has user data for the named workflow, out of the list of models selected by the user.
            If the workflow is run from REPORTER, it is the index in the list of all the models loaded in the session that 
            have user data for the named workflow
        workflow_name : string
            Optional. The workflow name to return the user data for

        Returns
        -------
        dict
            Dict
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelUserDataFromIndex", model_index, workflow_name)

    def ModelUserDataProgramFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the name of the program that was used to write out the
        user data of a model for the selected workflow by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the program name for
        workflow_name : string
            Optional. The workflow name to return the program name for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the program name for the first user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelUserDataProgramFromIndex", model_index, workflow_name)

    def ModelUserDataVersionFromIndex(model_index, workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the version of the program that was used to write out the
        user data of a model for the selected workflow by index (starting at 0)

        Parameters
        ----------
        model_index : integer
            The index of the model to return the program version for
        workflow_name : string
            Optional. The workflow name to return the version for. This is required when a PRIMER item is
            generated from REPORTER. If it is not specified the version for the first user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "ModelUserDataVersionFromIndex", model_index, workflow_name)

    def NumberOfSelectedModels(workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the number of models selected by the user

        Parameters
        ----------
        workflow_name : string
            Optional. The workflow name to return the number of models for.
            If it's not defined the number of models that were selected by the user on the workflow menu is returned.
            If it's defined and the workflow was run from the workflow menu, the number of models, out of the models selected by the user, that have data for the named workflow is returned.
            If it's defined and the workflow is run from REPORTER, the number of models, out of all the models loaded in the session, that have data for the named workflow is returned

        Returns
        -------
        int
            integer
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "NumberOfSelectedModels", workflow_name)

    def Refresh():
        """
        Scan for fresh workflow data

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Refresh")

    def WorkflowDefinitionFilename(workflow_name=Oasys.gRPC.defaultArg):
        """
        Returns the workflow definition filename

        Parameters
        ----------
        workflow_name : string
            Optional. The workflow name to return the workflow defintion filename for. This is required when a POST item is
            generated from REPORTER. If it is not specified the first workflow user data associated with 
            the model is returned (this is the 'normal' case where a user launches a workflow from the workflow
            menu)

        Returns
        -------
        str
            string
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "WorkflowDefinitionFilename", workflow_name)

    def WriteToFile(user_data, output_filename, workflow_definition_filename, extra=Oasys.gRPC.defaultArg):
        """
        Writes a workflow to a JSON file. If the file already exists the workflow
        is added to the file (or updated if it is already in the file)

        Parameters
        ----------
        user_data : object
            Object containing user data required for the workflow
        output_filename : string
            Filename to write to
        workflow_definition_filename : string
            Filename of the workflow definition file
        extra : dict
            Optional. Extra workflow information

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "WriteToFile", user_data, output_filename, workflow_definition_filename, extra)

