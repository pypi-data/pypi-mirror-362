"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
from pathlib import Path

DIR_PATH = Path(__file__).parent
modules = [Path(module).stem for module in DIR_PATH.glob("*.py")]
__all__ = [ f for f in modules if f != "__init__"]
