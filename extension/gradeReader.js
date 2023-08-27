import fs from "fs/promises";
import { open } from 'node:fs/promises';

import PDFParser from "pdf2json";







//CALL IT LIKE THIS:
//saveTranscriptJSON("Sxxxxxxx_UNOFFICIAL_TRANSCRIPT_009306055.pdf", "Grades.json")

/**
 * 
 * @param {:} pdf_path Path to academic transcript PDF
 * @param {*} output_path Path of output file
 */
async function saveTranscriptJSON(pdf_path, output_path) {
   let tempFile = await read("temp.txt");
    if (!tempFile) {
        await fs.writeFile("temp.txt", "");
    } 

    const pdfParser = new PDFParser(this,1);
    await pdfParser.loadPDF(pdf_path);

    await new Promise((resolve, reject) => {
        pdfParser.on("pdfParser_dataError", errData => {
            console.error(errData.parserError);
            reject(errData.parserError);
        });

        pdfParser.on("pdfParser_dataReady", async pdfData => {
            await fs.writeFile("temp.txt", pdfParser.getRawTextContent());
            resolve();
        });
    });
    let JSONString = JSON.stringify(await myFileReader("temp.txt"));

    await fs.writeFile(output_path, JSONString);
    await fs.unlink("temp.txt")
}

async function myFileReader(txtpath) {
    const file = await open(txtpath);
    let gradeLines = [];
    for await (const line of file.readLines()) {
        const numberOfDigits = line.replace(/[^0-9]/g,"").length
        if (numberOfDigits > 15 && numberOfDigits < 18) {
            gradeLines.push(line);
        }
    }
    gradeLines = gradeLines.map(data => {
        return {
            course_type: data.slice(0, 4),
            course_num: data.slice(9, 13),
            grade: data.slice(68, 69)
        }
    });
    return {academic_transcript: gradeLines};
}

async function read(filePath) {
    try {
        const data = await fs.readFile(filePath);
        return data;
    }
    catch (error) {
        return undefined;
    }
}