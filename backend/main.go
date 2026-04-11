package main

import (
	"fmt"
	"bytes"
	"encoding/base64"
)


// write a struct ( class ) for the server 
type Server struct {
	pb.UnimplementedDiagnosticServiceServer // this is a placeholder for the server 
}

// implement the GetDiagnostic method that belongs to the Server struct
func (s *Server) GetDiagnostic(ctx context.Context, req *pb.GetDiagnosticRequest) (*pb.GetDiagnosticResponse, error) {
	// two variables we might get from the client:
	var image bytes.Buffer
	var clinicalHistory string

	fmt.printLn("recieeved the x-ray chunks ")

	// step 1: the streaming for loop

	for {
		req , err := stream.Recv()

		// break the loop if there no recieved data
		if err == io.EOF {
			break
		}

		// break the loop if an error is received
		if err != nil {
			return nil, status.Errorf(codes.Internal, "error while recieving the x-ray chunks: %v", err)
		}

		// append the recieved chunk to the image
		imageBuffer.Write(req.GetImage())

		//  append the clinical history if it's there 
		if req.GetClinicalHistory() != "" {
			clinicalHistory = req.GetClinicalHistory()
		}

		//  break the loop if the last chunk is received
		if req.GetIsLastChunk() {
			break
		}

		// build the image, encoded to base64 string 
		iamgeBase64 := base64.StdEncoding.EncodeToString(imageBuffer.Bytes())

		// send stream that we have recieved the image
		stream.send(
			&pb.GetDiagnosticResponse{
				message: "image recieved",
			}
		)
	}
}

// function to send the image to the vision model, and get the diagnosis 
func sendImageToGemma(imageBase64 string) (string, error) {
	openRouterApiKey := os.Getenv("OPENROUTER_API_KEY")
	gemmaUrl := "https://openrouter.ai/api/v1/chat/completions"
	model := "google/gemini-2.5-flash"

	// payload, set stream to true 
	payload := map[string]interface{} {
		"model":model,
		"stream":true,
		"messages":[]map[string]interface{}{
			{
				"role":"user",
				"content":[]map[string]interface{}{
					{
						"type":"image_url",
						"image_url":map[string]interface{}{
							"url":fmt.Sprintf("data:image/jpeg;base64,%s", imageBase64),
						},
					},
				},
				"system": "You are a radiologist. You are given an x-ray image with or without a clinical history. \n
				You need to diagnose the patient based on the image and the clinical history. \n
				provide location of the fracture if any, and the type of fracture if any. \n
				provide the diagnosis in a json format with the following fields: \n
				- diagnosis: the diagnosis of the patient \n
				- location: the location of the fracture if any \n
				- type: the type of fracture if any \n
				- severity: the severity of the fracture if any \n
				- treatment: the treatment plan for the patient \n
				- prognosis: the prognosis for the patient \n
				- recommendation: the recommendation for the patient \n
				- note: any additional notes or comments \n
			},
		},
		"max_tokens":1000,
		"temperature":0.7,
		"top_p":1,	
		"frequency_penalty":0,
		"presence_penalty":0,
		"n":1,
		"stop":[]string{},
		"stream_options":map[string]interface{}{
			"include_usage":true,
		},
	}
	
}

func main() {
	// fmt.Println("Hello, World!")

	// step 1: recieve the image from the client 


}

