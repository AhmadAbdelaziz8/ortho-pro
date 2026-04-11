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
func sendImageToVisionModel(imageBase64 string) (string, error) {
	// step 1: send the image to the vision model

}


func main() {
	// fmt.Println("Hello, World!")

	// step 1: recieve the image from the client 


}

