
/**
 * Tests for L{Mantissa.LiveForm}.
 */

// import Divmod.UnitTest
// import Mantissa.LiveForm

/**
 * Tests for L{Mantissa.LiveForm.FormWidget}.
 */
Mantissa.Test.TestLiveForm.FormWidgetTests = Divmod.UnitTest.TestCase.subclass(
    'Mantissa.Test.TestLiveForm.FormWidgetTests');
Mantissa.Test.TestLiveForm.FormWidgetTests.methods(
    /**
     * Create a L{Mantissa.LiveForm.FormWidget} with a simple node.
     */
    function setUp(self) {
        self.node = document.createElement('span');
        self.node.id = 'athena:123';
        document.body.appendChild(self.node);
        self.widget = Mantissa.LiveForm.FormWidget(self.node);
        self.progressMessage = 'visible';
        self.widget.hideProgressMessage = function() {
            self.progressMessage = 'hidden';
        };
    },

    /**
     * Remove from the document the node which was added by setUp.
     */
    function tearDown(self) {
        document.body.removeChild(self.node);
    },

    /**
     * L{Mantissa.LiveForm.FormWidget.submitFailure} should dispatch
     * L{Mantissa.LiveForm.InputError} errors to
     * L{Mantissa.LiveForm.FormWidget.displayInputError}.
     */
    function test_handleInputErrorFailure(self) {
        var error = Mantissa.LiveForm.InputError("bogus input");
        var failure = Divmod.Defer.Failure(error);
        var inputErrors = [];
        self.widget.displayInputError = function stubDisplayInputError(err) {
            inputErrors.push(err);
        };
        self.widget.submitFailure(failure);
        self.assertIdentical(inputErrors.length, 1);
        self.assertIdentical(inputErrors[0], error);
        self.assertIdentical(self.progressMessage, 'hidden');
    },

    /**
     * L{Mantissa.LiveForm.FormWidget.submitFailure} should not dispatch
     * exceptions which do not derive from L{Mantissa.LiveForm.InputError} to
     * L{Mantissa.LiveForm.FormWidget.displayInputError}.
     */
    function test_handleOtherFailure(self) {
        var failure = Divmod.Defer.Failure(Divmod.Error("random failure"));
        var inputErrors = [];
        self.widget.displayInputError = function stubDisplayInputError(err) {
            inputErrors.push(err);
        };
        self.widget.submitFailure(failure);
        self.assertIdentical(inputErrors.length, 0);
        self.assertIdentical(self.progressMessage, 'hidden');
    },

    /**
     * L{Mantissa.LiveForm.FormWidget.displayInputError} should replace the
     * contents of the node beneath the widget with the I{class} of
     * I{input-error-message} with the string of the failure.
     */
    function test_displayInputError(self) {
        var messageNode = document.createElement('span');
        messageNode.id = 'athenaid:123-input-error-message';
        messageNode.appendChild(document.createElement('span'));
        self.node.appendChild(messageNode);
        self.widget.displayInputError(
            Mantissa.LiveForm.InputError('bogus input'));
        self.assertIdentical(messageNode.childNodes.length, 1);
        self.assertIdentical(
            messageNode.childNodes[0].nodeValue,
            'bogus input');
    },

    /**
     * L{Mantissa.LiveForm.FormWidget.displayInputError} should do nothing if
     * no status node can be found.
     */
    function test_missingStatusNode(self) {
        self.widget.displayInputError(
            Mantissa.LiveForm.InputError('bogus input'));
        self.assertIdentical(
            self.widget.node.childNodes.length, 0);
    });