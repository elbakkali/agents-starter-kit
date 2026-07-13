"""Scaffold Laravel API endpoint stubs when a Laravel app exists."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "api"


def studly(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[-_\s]+", name) if part)


def main() -> None:
    if not (API / "artisan").exists():
        print("Skip: no Laravel app in api/ (run laravel new or composer create-project first).")
        sys.exit(0)

    resource = " ".join(sys.argv[1:]).strip()
    if not resource:
        resource = input("Resource name (e.g. invoice): ").strip()
    if not resource:
        print("Resource name required.", file=sys.stderr)
        sys.exit(1)

    class_name = studly(resource)
    controller = API / "app" / "Http" / "Controllers" / f"{class_name}Controller.php"
    request = API / "app" / "Http" / "Requests" / f"Store{class_name}Request.php"
    test = API / "tests" / "Feature" / f"{class_name}Test.php"

    if controller.exists():
        print(f"Already exists: {controller}", file=sys.stderr)
        sys.exit(1)

    controller.parent.mkdir(parents=True, exist_ok=True)
    request.parent.mkdir(parents=True, exist_ok=True)
    test.parent.mkdir(parents=True, exist_ok=True)

    controller.write_text(
        f"""<?php

namespace App\\Http\\Controllers;

use App\\Http\\Requests\\Store{class_name}Request;
use Illuminate\\Http\\JsonResponse;

class {class_name}Controller extends Controller
{{
    public function store(Store{class_name}Request $request): JsonResponse
    {{
        // TODO: delegate to action/service
        return response()->json(['message' => 'Created'], 201);
    }}
}}
""",
        encoding="utf-8",
    )

    request.write_text(
        f"""<?php

namespace App\\Http\\Requests;

use Illuminate\\Foundation\\Http\\FormRequest;

class Store{class_name}Request extends FormRequest
{{
    public function authorize(): bool
    {{
        return true;
    }}

    public function rules(): array
    {{
        return [
            // TODO: validation rules
        ];
    }}
}}
""",
        encoding="utf-8",
    )

    test.write_text(
        f"""<?php

use Illuminate\\Foundation\\Testing\\RefreshDatabase;

uses(RefreshDatabase::class);

it('creates a {resource}', function () {{
    // TODO: implement feature test
    $this->markTestIncomplete('Scaffolded — implement after spec approval');
}});
""",
        encoding="utf-8",
    )

    print(f"Created: {controller.relative_to(ROOT)}")
    print(f"Created: {request.relative_to(ROOT)}")
    print(f"Created: {test.relative_to(ROOT)}")
    print(f"Add route in api/routes/api.php: Route::post('/{resource}s', [{class_name}Controller::class, 'store']);")
    print("Document endpoint in docs/technical/api-contract.md after implementation.")


if __name__ == "__main__":
    main()
