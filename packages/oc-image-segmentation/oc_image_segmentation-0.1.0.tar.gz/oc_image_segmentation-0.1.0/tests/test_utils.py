#!/usr/bin/env python3
"""
Tests for the module utils of oc_image_segmentation.

Ce test filee the utilitaires généraux of the projet :
- Gestion some erreurs and débogage
- Décorateurs of exception
- Fonctions utilitaires
- Visualisation of historique of entraînement

Convention of nommage : test_[fonctionnalité]
"""

import logging
from unittest.mock import MagicMock, patch

import pytest

from oc_image_segmentation.config import reset_settings_with_files
from oc_image_segmentation.utils import (
    handle_exceptions,
    is_debug_mode,
    plot_history,
    safe_execute,
    with_error_logging,
)


class TestDebugMode:
    """Tests for the fonction is_debug_mode."""

    def test_debug_mode_enabled(self):
        """Test quand DEBUG est activé."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", True):
            assert is_debug_mode() is True

    def test_debug_mode_disabled(self):
        """Test quand DEBUG est désactivé."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", False):
            assert is_debug_mode() is False

    def test_debug_mode_not_set(self):
        """Test quand DEBUG n'est pas défini."""
        # Supprimer the attribut DEBUG s'il existe
        settings = reset_settings_with_files()
        if hasattr(settings, "DEBUG"):
            delattr(settings, "DEBUG")
        assert is_debug_mode() is False


class TestHandleExceptions:
    """Tests for the décorateur handle_exceptions."""

    def test_successful_execution(self):
        """Test with a fonction which s'exécute without erreur."""

        @handle_exceptions(default_return="default")
        def successful_func():
            return "success"

        result = successful_func()
        assert result == "success"

    def test_exception_handling_debug_false(self):
        """Test of gestion of exception with DEBUG=False."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", False):

            @handle_exceptions(default_return="default")
            def failing_func():
                raise ValueError("Test error")

            result = failing_func()
            assert result == "default"

    def test_exception_handling_debug_true(self):
        """Test of gestion of exception with DEBUG=True."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", True):

            @handle_exceptions(default_return="default", reraise_on_debug=True)
            def failing_func():
                raise ValueError("Test error")

            with pytest.raises(ValueError, match="Test error"):
                failing_func()

    def test_exception_no_reraise_debug_true(self):
        """Test without re-lever the exception même with DEBUG=True."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", True):

            @handle_exceptions(default_return="default", reraise_on_debug=False)
            def failing_func():
                raise ValueError("Test error")

            result = failing_func()
            assert result == "default"


class TestSafeExecute:
    """Tests for the fonction safe_execute."""

    def test_safe_execute_success(self):
        """Test of exécution réussie with safe_execute."""

        def test_func(x, y):
            return x + y

        result = safe_execute(test_func, 2, 3)
        assert result == 5

    def test_safe_execute_with_kwargs(self):
        """Test with some arguments by mots-clés."""

        def test_func(x, y=10):
            return x * y

        result = safe_execute(test_func, 5, y=3)
        assert result == 15

    def test_safe_execute_exception_debug_false(self):
        """Test of gestion of exception with DEBUG=False."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", False):

            def failing_func():
                raise RuntimeError("Test error")

            result = safe_execute(
                failing_func, default_return="fallback", log_message="Operation failed"
            )
            assert result == "fallback"

    def test_safe_execute_exception_debug_true(self):
        """Test of gestion of exception with DEBUG=True."""
        settings = reset_settings_with_files()
        with patch.object(settings, "DEBUG", True):

            def failing_func():
                raise RuntimeError("Test error")

            with pytest.raises(RuntimeError, match="Test error"):
                safe_execute(
                    failing_func, default_return="fallback", reraise_on_debug=True
                )


class TestErrorLogging:
    """Tests for the décorateur with_error_logging."""

    @patch("oc_image_segmentation.utils.logger")
    def test_error_logging_success(self, mock_logger):
        """Test without exception."""

        @with_error_logging()
        def successful_func():
            return "success"

        result = successful_func()
        assert result == "success"
        mock_logger.log.assert_not_called()

    @patch("oc_image_segmentation.utils.logger")
    def test_error_logging_with_error(self, mock_logger):
        """Test with exception."""

        @with_error_logging(log_level=logging.ERROR, message="Test failed")
        def failing_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            failing_func()

        mock_logger.log.assert_called_once()
        call_args = mock_logger.log.call_args
        assert call_args[0][0] == logging.ERROR
        assert "Test failed" in call_args[0][1]
        assert "failing_func" in call_args[0][1]


class TestPlotHistory:
    """Tests for the fonction plot_history."""

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.plot")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.grid")
    def test_plot_history_success(
        self,
        mock_grid,
        mock_legend,
        mock_ylabel,
        mock_xlabel,
        mock_title,
        mock_plot,
        mock_figure,
        mock_show,
    ):
        """Test of plot_history with a historique valide."""
        # Mock of a objet historique
        mock_history = MagicMock()
        mock_history.history = {
            "loss": [0.5, 0.3, 0.2],
            "val_loss": [0.6, 0.4, 0.3],
            "accuracy": [0.8, 0.9, 0.95],
            "val_accuracy": [0.7, 0.85, 0.9],
        }

        plot_history(mock_history)

        # Verify that The functions matplotlib have been called
        assert mock_figure.call_count == 4
        assert mock_plot.call_count == 4
        assert mock_show.call_count == 2

    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.figure")
    @patch("matplotlib.pyplot.plot")
    def test_plot_history_empty_metrics(
        self,
        mock_plot,
        mock_figure,
        mock_show,
    ):
        """Test with a historique without métriques."""
        mock_history = MagicMock()
        mock_history.history = {"val_loss": [0.5, 0.3]}  # Seulement val_*

        mock_figure.reset_mock()  # !!

        # not devrait pas lever of exception
        plot_history(mock_history)

        # Verify that The functions matplotlib have been called
        assert mock_figure.call_count == 7
        assert mock_plot.call_count == 1
        assert mock_show.call_count == 1


if __name__ == "__main__":
    pytest.main([__file__])
