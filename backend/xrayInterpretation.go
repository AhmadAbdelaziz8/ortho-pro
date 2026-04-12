package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"google.golang.org/genai"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type Finding struct {
	Name     string `json:"name"`
	Location string `json:"location"`
	Severity string `json:"severity"`
}

type Classification struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	Grade       string `json:"grade"`
}

type XrayDiagnosis struct {
	BoneName       string         `json:"bone_name"`
	Findings       []Finding      `json:"findings"`
	Classification Classification `json:"classification"`
	Diagnosis      string         `json:"diagnosis"`
}

func getImageDiagnosis(imageBytes []byte, clinicalHistory string) (*XrayDiagnosis, error) {
	if os.Getenv("GEMINI_API_KEY") == "" {
		return nil, status.Error(codes.Internal, "GEMINI_API_KEY is not set")
	}

	ctx := context.Background()
	model := "gemini-3-flash-preview"

	client, err := genai.NewClient(ctx, nil)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "error while creating Gemini client: %v", err)
	}

	schema := map[string]any{
		"type":                 "object",
		"additionalProperties": false,
		"properties": map[string]any{
			"bone_name": map[string]any{
				"type":        "string",
				"description": "Main bone involved in the injury, for example tibia, fibula, radius, ulna, humerus, or femur.",
			},
			"findings": map[string]any{
				"type":        "array",
				"description": "Important imaging findings seen on the X-ray.",
				"items": map[string]any{
					"type":                 "object",
					"additionalProperties": false,
					"properties": map[string]any{
						"name": map[string]any{
							"type":        "string",
							"description": "Name of the imaging finding, for example fracture, dislocation, lytic lesion, or joint effusion.",
						},
						"location": map[string]any{
							"type":        "string",
							"description": "Anatomical location of the finding.",
						},
						"severity": map[string]any{
							"type":        "string",
							"description": "Severity or extent if visible, for example mild, moderate, severe, displaced, or non-displaced.",
						},
					},
					"required": []string{"name", "location", "severity"},
				},
			},
			"classification": map[string]any{
				"type":                 "object",
				"additionalProperties": false,
				"description":          "Fracture or injury classification when applicable. Use empty strings if no classification applies.",
				"properties": map[string]any{
					"name": map[string]any{
						"type":        "string",
						"description": "Classification system name, for example Gartland, AO, or Salter-Harris.",
					},
					"description": map[string]any{
						"type":        "string",
						"description": "Short explanation of the classification result.",
					},
					"grade": map[string]any{
						"type":        "string",
						"description": "Classification grade or type, for example type II, 42-A1, or Salter-Harris II.",
					},
				},
				"required": []string{"name", "description", "grade"},
			},
			"diagnosis": map[string]any{
				"type":        "string",
				"description": "Single concise radiology-style diagnosis or impression.",
			},
		},
		"required": []string{"bone_name", "findings", "classification", "diagnosis"},
	}

	config := &genai.GenerateContentConfig{
		ResponseMIMEType:   "application/json",
		ResponseJsonSchema: schema,
	}

	prompt := fmt.Sprintf(`
You are assisting with structured extraction from an orthopaedic X-ray.

Clinical history:
%s

Instructions:
- Analyze the image and return only the JSON fields requested by the schema.
- Be cautious and do not invent findings not visible on the image.
- If no fracture classification applies, keep classification fields as empty strings.
- Keep "diagnosis" short and clinically useful.
`, clinicalHistory)

	parts := []*genai.Part{
		genai.NewPartFromBytes(imageBytes, "image/jpeg"), // change to image/png if needed
		genai.NewPartFromText(prompt),
	}

	contents := []*genai.Content{
		genai.NewContentFromParts(parts, genai.RoleUser),
	}

	result, err := client.Models.GenerateContent(ctx, model, contents, config)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "Gemini request failed: %v", err)
	}

	var diagnosis XrayDiagnosis
	if err := json.Unmarshal([]byte(result.Text()), &diagnosis); err != nil {
		return nil, status.Errorf(codes.Internal, "failed to parse structured JSON: %v; raw=%s", err, result.Text())
	}

	return &diagnosis, nil
}
