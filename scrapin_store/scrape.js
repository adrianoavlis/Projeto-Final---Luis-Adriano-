const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const winston = require('winston');

// Configuração do logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) => `${timestamp} - ${level}: ${message}`)
    ),
    transports: [
        new winston.transports.File({ filename: 'scraping_indeed.log' })
    ]
});

// Função para extrair dados de um emprego
const extractJobData = (job) => {
    try {
        const title = job.find('h2.title').text().trim();
        const company = job.find('span.company').text().trim();
        const location = job.find('div.location').text().trim() || 'N/A';
        const summary = job.find('div.summary').text().trim();
        const jobLink = 'https://www.indeed.com' + job.find('a').attr('href');
        
        return {
            title,
            company,
            location,
            summary,
            jobLink
        };
    } catch (error) {
        logger.error(`Erro ao extrair dados do emprego: ${error.message}`);
        return null;
    }
};

// Função para fazer scraping de múltiplas páginas de resultados com retries
const scrapeIndeedJobs = async (query, location, numPages) => {
    const baseUrl = 'https://www.indeed.com/jobs';
    const allJobs = [];
    const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36';
    const maxRetries = 5;

    for (let page = 0; page < numPages * 10; page += 10) {
        const params = { q: query, l: location, start: page };
        let success = false;
        let attempts = 0;

        while (!success && attempts < maxRetries) {
            try {
                const response = await axios.get(baseUrl, { params, headers: { 'User-Agent': userAgent } });
                const $ = cheerio.load(response.data);
                const jobCards = $('div.jobsearch-SerpJobCard');

                jobCards.each((i, elem) => {
                    const jobData = extractJobData($(elem));
                    if (jobData) allJobs.push(jobData);
                });

                logger.info(`Página ${(page / 10) + 1} raspada com sucesso.`);
                success = true;
                await new Promise(resolve => setTimeout(resolve, 2000)); // Pausa de 2 segundos entre as requisições
            } catch (error) {
                attempts++;
                logger.error(`Erro ao acessar a página ${(page / 10) + 1} (tentativa ${attempts}): ${error.message}`);
                if (attempts >= maxRetries) {
                    logger.error(`Falha ao acessar a página ${(page / 10) + 1} após ${maxRetries} tentativas. Abortando.`);
                    break;
                }
                await new Promise(resolve => setTimeout(resolve, 2000)); // Pausa de 2 segundos antes de tentar novamente
            }
        }

        if (!success) {
            break;
        }
    }

    return allJobs;
};

// Função para salvar os dados em um arquivo CSV
const saveJobsToCsv = async (jobs, filename) => {
    const csvWriter = createCsvWriter({
        path: filename,
        header: [
            { id: 'title', title: 'Título' },
            { id: 'company', title: 'Empresa' },
            { id: 'location', title: 'Localização' },
            { id: 'summary', title: 'Resumo' },
            { id: 'jobLink', title: 'Link' }
        ]
    });

    try {
        await csvWriter.writeRecords(jobs);
        logger.info(`Dados salvos em ${filename} com sucesso.`);
    } catch (error) {
        logger.error(`Erro ao salvar dados em ${filename}: ${error.message}`);
    }
};

// Configurações de busca
const query = 'python developer';
const location = '';
const numPages = 5; // Número de páginas para scrape

// Executa o scraping
(async () => {
    try {
        const jobs = await scrapeIndeedJobs(query, location, numPages);
        if (jobs.length > 0) {
            await saveJobsToCsv(jobs, 'indeed_jobs.csv');
            console.log(`Scraping concluído! Dados salvos em 'indeed_jobs.csv'.`);
        } else {
            logger.warn('Nenhum dado de emprego foi coletado.');
        }
    } catch (error) {
        logger.error(`Erro crítico durante o scraping: ${error.message}`);
        console.log('Erro crítico durante o scraping. Consulte o arquivo de log para mais detalhes.');
    }
})();
